#!/usr/bin/env python3
"""Run a CPU-only AWS Batch smoke test using persistent, reusable Batch resources.

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

VPC_SUBNET = "subnet-b560b3fd"
SECURITY_GROUP = "sg-bd00e4f5"
TERMINAL_STATES = {"SUCCEEDED", "FAILED"}


def wait_for(get_status, expected, timeout, description):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        status = get_status()
        print(f"  {description}: {status}")
        if status in expected:
            return status
        time.sleep(10)
    raise TimeoutError(f"Timed out waiting for {description}")


def ensure_compute_environment(batch, name, compute_resources, timeout):
    """Reuse the named compute environment, creating it only if missing."""
    environments = batch.describe_compute_environments(
        computeEnvironments=[name]
    ).get("computeEnvironments", [])
    if environments:
        environment = environments[0]
        print(f"Reusing compute environment: {name}")
        existing = environment.get("computeResources", {})
        expected_types = set(compute_resources.get("instanceTypes", []))
        if existing.get("type") != compute_resources["type"] or set(
            existing.get("instanceTypes", [])
        ) != expected_types:
            raise RuntimeError(
                f"Compute environment {name} already exists with type="
                f"{existing.get('type')} instanceTypes={existing.get('instanceTypes')}"
                f" — expected type={compute_resources['type']}"
                f" instanceTypes={sorted(expected_types)}."
                " Fix or remove it manually before running the smoke test."
            )
        if environment["state"] != "ENABLED":
            print(f"  Re-enabling compute environment: {name}")
            batch.update_compute_environment(computeEnvironment=name, state="ENABLED")
    else:
        print(f"Creating compute environment: {name}")
        batch.create_compute_environment(
            computeEnvironmentName=name,
            type="MANAGED",
            state="ENABLED",
            computeResources=compute_resources,
        )
    status = wait_for(
        lambda: batch.describe_compute_environments(computeEnvironments=[name])[
            "computeEnvironments"
        ][0]["status"],
        {"VALID", "INVALID"},
        timeout,
        "Compute environment",
    )
    if status != "VALID":
        raise RuntimeError(
            f"Compute environment {name} is INVALID — fix or remove it manually"
        )


def ensure_job_queue(batch, name, environment_name, timeout):
    """Reuse the named job queue (bound to environment_name), creating it if missing."""
    queues = batch.describe_job_queues(jobQueues=[name]).get("jobQueues", [])
    if queues:
        queue = queues[0]
        print(f"Reusing job queue: {name}")
        order_arn = queue["computeEnvironmentOrder"][0]["computeEnvironment"]
        if not order_arn.endswith(f"compute-environment/{environment_name}"):
            raise RuntimeError(
                f"Job queue {name} is bound to {order_arn}, expected compute"
                f" environment {environment_name}. Fix or remove the queue manually."
            )
        if queue["state"] != "ENABLED":
            print(f"  Re-enabling job queue: {name}")
            batch.update_job_queue(jobQueue=name, state="ENABLED")
    else:
        print(f"Creating job queue: {name}")
        batch.create_job_queue(
            jobQueueName=name,
            state="ENABLED",
            priority=1,
            computeEnvironmentOrder=[{"order": 1, "computeEnvironment": environment_name}],
        )
    status = wait_for(
        lambda: batch.describe_job_queues(jobQueues=[name])["jobQueues"][0]["status"],
        {"VALID", "INVALID"},
        timeout,
        "Job queue",
    )
    if status != "VALID":
        raise RuntimeError(f"Job queue {name} is INVALID — fix or remove it manually")


def main():
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    parser = argparse.ArgumentParser(
        description="Run a CPU-only AWS Batch smoke test using persistent resources."
    )
    parser.add_argument("--region", default=os.environ.get("AWS_DEFAULT_REGION", "ap-northeast-1"))
    parser.add_argument("--instance-profile", default="ecsInstanceRole",
                        help="EC2 instance profile name used by Batch (default: ecsInstanceRole)")
    parser.add_argument("--timeout", type=int, default=900,
                        help="Seconds to wait for environment and job completion (default: 900)")
    args = parser.parse_args()

    environment_name = "gpu-teaching-cpu-smoke-ce"
    queue_name = "gpu-teaching-cpu-smoke-queue"
    definition_name = "gpu-teaching-cpu-smoke-job"
    batch = boto3.client("batch", region_name=args.region)
    account_id = boto3.client("sts", region_name=args.region).get_caller_identity()["Account"]
    instance_profile = f"arn:aws:iam::{account_id}:instance-profile/{args.instance_profile}"

    ensure_compute_environment(
        batch,
        environment_name,
        {
            "type": "EC2",
            "minvCpus": 0,
            "maxvCpus": 2,
            "instanceTypes": ["c6a.large"],
            "subnets": [VPC_SUBNET],
            "securityGroupIds": [SECURITY_GROUP],
            "instanceRole": instance_profile,
        },
        args.timeout,
    )
    ensure_job_queue(batch, queue_name, environment_name, args.timeout)

    definition_arn = batch.register_job_definition(
        jobDefinitionName=definition_name,
        type="container",
        containerProperties={
            "image": "public.ecr.aws/docker/library/busybox:latest",
            "vcpus": 1,
            "memory": 128,
            "command": ["sh", "-c", "echo CPU Batch smoke test passed"],
        },
    )["jobDefinitionArn"]
    job_id = batch.submit_job(
        jobName="cpu-smoke", jobQueue=queue_name, jobDefinition=definition_arn
    )["jobId"]
    print(f"Submitted CPU smoke job: {job_id}")
    status = wait_for(
        lambda: batch.describe_jobs(jobs=[job_id])["jobs"][0]["status"],
        TERMINAL_STATES,
        args.timeout,
        "CPU smoke job",
    )
    if status != "SUCCEEDED":
        raise RuntimeError(f"CPU smoke job finished with {status}")
    print("CPU Batch smoke test passed.")


if __name__ == "__main__":
    try:
        main()
    except (ClientError, RuntimeError, TimeoutError) as error:
        print(f"CPU Batch smoke test failed: {error}", file=sys.stderr)
        sys.exit(1)
