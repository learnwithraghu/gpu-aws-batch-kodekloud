#!/usr/bin/env python3
"""Run a disposable GPU AWS Batch smoke test (Spot or On-Demand) and remove its resources."""

import argparse
import os
import sys
import time
import uuid

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

from test_cpu_batch import SECURITY_GROUP, TERMINAL_STATES, VPC_SUBNET, cleanup, wait_for


def main():
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    parser = argparse.ArgumentParser(description="Run and clean up a GPU AWS Batch smoke test.")
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

    suffix = uuid.uuid4().hex[:8]
    environment_name = f"gpu-teaching-gpu-smoke-ce-{suffix}"
    queue_name = f"gpu-teaching-gpu-smoke-queue-{suffix}"
    definition_name = f"gpu-teaching-gpu-smoke-job-{suffix}"
    batch = boto3.client("batch", region_name=args.region)
    job_id = None
    definition_arn = None
    environment_created = False
    queue_created = False
    account_id = boto3.client("sts", region_name=args.region).get_caller_identity()["Account"]
    instance_profile = f"arn:aws:iam::{account_id}:instance-profile/{args.instance_profile}"
    try:
        print(f"Creating GPU compute environment ({args.capacity_type}): {environment_name}")
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
        batch.create_compute_environment(
            computeEnvironmentName=environment_name,
            type="MANAGED",
            state="ENABLED",
            computeResources=compute_resources,
        )
        environment_created = True
        environment_status = wait_for(
            lambda: batch.describe_compute_environments(computeEnvironments=[environment_name])[
                "computeEnvironments"
            ][0]["status"],
            {"VALID", "INVALID"},
            args.timeout,
            "Compute environment",
        )
        if environment_status != "VALID":
            raise RuntimeError("GPU compute environment became INVALID")

        batch.create_job_queue(
            jobQueueName=queue_name,
            state="ENABLED",
            priority=1,
            computeEnvironmentOrder=[{"order": 1, "computeEnvironment": environment_name}],
        )
        queue_created = True
        queue_status = wait_for(
            lambda: batch.describe_job_queues(jobQueues=[queue_name])["jobQueues"][0]["status"],
            {"VALID", "INVALID"},
            args.timeout,
            "Job queue",
        )
        if queue_status != "VALID":
            raise RuntimeError("GPU job queue became INVALID")

        definition_arn = batch.register_job_definition(
            jobDefinitionName=definition_name,
            type="container",
            containerProperties={
                "image": "public.ecr.aws/nvidia/cuda:12.6.3-base-ubuntu22.04",
                "vcpus": 1,
                "memory": 1024,
                "resourceRequirements": [{"type": "GPU", "value": "1"}],
                "command": ["sh", "-c", "nvidia-smi && echo GPU Batch smoke test passed"],
            },
        )["jobDefinitionArn"]
        job_id = batch.submit_job(
            jobName=f"gpu-smoke-{suffix}", jobQueue=queue_name, jobDefinition=definition_arn
        )["jobId"]
        print(f"Submitted GPU smoke job: {job_id}")

        # ── Provisioning timer: 3 min to move from SUBMITTED/RUNNABLE to RUNNING ──
        PROVISION_TIMEOUT = 180  # 3 minutes
        deadline = time.monotonic() + PROVISION_TIMEOUT
        provisioning_ok = False
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
            print(f"\n⏱️  Provisioning timed out after {PROVISION_TIMEOUT}s — cleaning up.")
            raise TimeoutError(
                f"Instance not provisioned within {PROVISION_TIMEOUT}s "
                f"(job stayed in {status}); the job will be terminated and resources cleaned up."
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
    finally:
        cleanup(
            batch,
            job_id,
            queue_name if queue_created else None,
            environment_name if environment_created else None,
            definition_arn,
        )


if __name__ == "__main__":
    try:
        main()
    except (ClientError, RuntimeError, TimeoutError) as error:
        print(f"GPU Batch smoke test failed: {error}", file=sys.stderr)
        sys.exit(1)