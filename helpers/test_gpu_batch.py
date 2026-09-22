#!/usr/bin/env python3
"""Run a GPU AWS Batch smoke test (Spot or On-Demand) using persistent Batch resources.

The compute environment, job queue, and job definition are created once with
stable names and reused on every run — this script never deletes them, so
repeat runs skip the create/wait/delete cycle and finish much faster.
Use helpers/teardown.py to remove them when you are done with the course.
"""

import argparse
import os
import sys
import time

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

from test_cpu_batch import (
    SECURITY_GROUP,
    TERMINAL_STATES,
    VPC_SUBNET,
    ensure_compute_environment,
    ensure_job_queue,
    wait_for,
)


def main():
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    parser = argparse.ArgumentParser(
        description="Run a GPU AWS Batch smoke test using persistent resources."
    )
    parser.add_argument("--region", default=os.environ.get("AWS_DEFAULT_REGION", "ap-northeast-1"))
    parser.add_argument("--instance-profile", default="ecsInstanceRole",
                        help="EC2 instance profile name used by Batch (default: ecsInstanceRole)")
    parser.add_argument("--instance-type", default="g4dn.xlarge",
                        help="GPU instance type — NVIDIA T4 (default: g4dn.xlarge)")
    parser.add_argument("--capacity-type", choices=["spot", "on-demand"], default="on-demand",
                        help="Compute environment purchasing option to test (default: on-demand)")
    parser.add_argument("--timeout", type=int, default=900,
                        help="Seconds to wait for environment and job completion (default: 900)")
    args = parser.parse_args()

    environment_name = f"gpu-teaching-gpu-smoke-ce-{args.capacity_type}"
    queue_name = f"gpu-teaching-gpu-smoke-queue-{args.capacity_type}"
    definition_name = "gpu-teaching-gpu-smoke-job"
    batch = boto3.client("batch", region_name=args.region)
    account_id = boto3.client("sts", region_name=args.region).get_caller_identity()["Account"]
    instance_profile = f"arn:aws:iam::{account_id}:instance-profile/{args.instance_profile}"

    compute_resources = {
        "type": "SPOT" if args.capacity_type == "spot" else "EC2",
        "minvCpus": 0,
        "maxvCpus": 4,
        "instanceTypes": [args.instance_type],
        "subnets": [VPC_SUBNET],
        "securityGroupIds": [SECURITY_GROUP],
        "instanceRole": instance_profile,
    }
    if args.capacity_type == "spot":
        compute_resources["allocationStrategy"] = "SPOT_CAPACITY_OPTIMIZED"

    ensure_compute_environment(batch, environment_name, compute_resources, args.timeout)
    ensure_job_queue(batch, queue_name, environment_name, args.timeout)

    # register_job_definition is idempotent for an unchanged spec: Batch returns
    # the existing revision, so re-registering each run costs nothing.
    definition_arn = batch.register_job_definition(
        jobDefinitionName=definition_name,
        type="container",
        containerProperties={
            "image": "nvidia/cuda:12.6.3-runtime-ubuntu22.04",
            "vcpus": 1,
            "memory": 1024,
            "resourceRequirements": [{"type": "GPU", "value": "1"}],
            "command": ["sh", "-c", "nvidia-smi && echo GPU Batch smoke test passed"],
        },
    )["jobDefinitionArn"]
    job_id = batch.submit_job(
        jobName=f"gpu-smoke-{args.capacity_type}", jobQueue=queue_name, jobDefinition=definition_arn
    )["jobId"]
    print(f"Submitted GPU smoke job: {job_id}")

    # ── Provisioning timer: 3 min to move from SUBMITTED/RUNNABLE to RUNNING ──
    PROVISION_TIMEOUT = 180  # 3 minutes
    deadline = time.monotonic() + PROVISION_TIMEOUT
    provisioning_ok = False
    status = None
    while time.monotonic() < deadline:
        status = batch.describe_jobs(jobs=[job_id])["jobs"][0]["status"]
        print(f"  GPU smoke job (provisioning): {status}")
        if status == "RUNNING":
            provisioning_ok = True
            break
        if status in {"FAILED", "SUCCEEDED"}:
            break
        time.sleep(10)

    if not provisioning_ok:
        if status in {"FAILED", "SUCCEEDED"}:
            raise RuntimeError(f"GPU smoke job finished with {status} before reaching RUNNING")
        print(
            f"\n⏱️  Provisioning timed out after {PROVISION_TIMEOUT}s — terminating the job."
            " Persistent resources are kept."
        )
        batch.terminate_job(jobId=job_id, reason="GPU smoke test provisioning timeout")
        raise TimeoutError(
            f"Instance not provisioned within {PROVISION_TIMEOUT}s "
            f"(job stayed in {status}); the job was terminated."
        )

    # ── Wait for job completion (full timeout applies) ──
    status = wait_for(
        lambda: batch.describe_jobs(jobs=[job_id])["jobs"][0]["status"],
        TERMINAL_STATES,
        args.timeout,
        "GPU smoke job",
    )
    if status != "SUCCEEDED":
        raise RuntimeError(f"GPU smoke job finished with {status}")
    print(f"GPU Batch smoke test passed ({args.capacity_type}, {args.instance_type}).")


if __name__ == "__main__":
    try:
        main()
    except (ClientError, RuntimeError, TimeoutError) as error:
        print(f"GPU Batch smoke test failed: {error}", file=sys.stderr)
        sys.exit(1)
