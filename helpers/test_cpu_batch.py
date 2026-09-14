#!/usr/bin/env python3
"""Run a disposable CPU-only AWS Batch smoke test and remove its resources."""

import argparse
import os
import sys
import time
import uuid

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


def wait_until_missing(describe, timeout, description):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            response = describe()
            if not response.get("jobQueues", response.get("computeEnvironments", [True])):
                print(f"  {description}: deleted")
                return
            print(f"  {description}: deleting")
            time.sleep(10)
        except ClientError as error:
            if error.response["Error"]["Code"] in {"ClientException", "ResourceNotFoundException"}:
                print(f"  {description}: deleted")
                return
            raise
    raise TimeoutError(f"Timed out waiting for {description} deletion")


def cleanup(batch, job_id, queue_name, environment_name, definition_arn):
    print("\nCleaning up temporary CPU Batch resources...")
    if job_id:
        try:
            status = batch.describe_jobs(jobs=[job_id])["jobs"][0]["status"]
            if status not in TERMINAL_STATES:
                batch.terminate_job(jobId=job_id, reason="CPU smoke test cleanup")
                wait_for(
                    lambda: batch.describe_jobs(jobs=[job_id])["jobs"][0]["status"],
                    TERMINAL_STATES,
                    300,
                    "Job termination",
                )
        except ClientError as error:
            print(f"  Could not terminate job: {error}")

    if queue_name:
        try:
            batch.update_job_queue(jobQueue=queue_name, state="DISABLED")
            wait_for(
                lambda: "{state}/{status}".format(**batch.describe_job_queues(
                    jobQueues=[queue_name]
                )["jobQueues"][0]),
                {"DISABLED/VALID"},
                300,
                "Job queue disablement",
            )
            batch.delete_job_queue(jobQueue=queue_name)
            wait_until_missing(
                lambda: batch.describe_job_queues(jobQueues=[queue_name]),
                300,
                "Job queue",
            )
        except ClientError as error:
            print(f"  Could not delete job queue: {error}")

    if environment_name:
        try:
            batch.update_compute_environment(computeEnvironment=environment_name, state="DISABLED")
            wait_for(
                lambda: "{state}/{status}".format(**batch.describe_compute_environments(
                    computeEnvironments=[environment_name]
                )["computeEnvironments"][0]),
                {"DISABLED/VALID"},
                300,
                "Compute environment disablement",
            )
            batch.delete_compute_environment(computeEnvironment=environment_name)
            wait_until_missing(
                lambda: batch.describe_compute_environments(computeEnvironments=[environment_name]),
                300,
                "Compute environment",
            )
        except ClientError as error:
            print(f"  Could not delete compute environment: {error}")

    if definition_arn:
        try:
            batch.deregister_job_definition(jobDefinition=definition_arn)
        except ClientError as error:
            print(f"  Could not deregister job definition: {error}")


def main():
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    parser = argparse.ArgumentParser(description="Run and clean up a CPU-only AWS Batch smoke test.")
    parser.add_argument("--region", default=os.environ.get("AWS_DEFAULT_REGION", "ap-northeast-1"))
    parser.add_argument("--instance-profile", default="ecsInstanceRole",
                        help="EC2 instance profile name used by Batch (default: ecsInstanceRole)")
    parser.add_argument("--timeout", type=int, default=900,
                        help="Seconds to wait for environment and job completion (default: 900)")
    args = parser.parse_args()

    suffix = uuid.uuid4().hex[:8]
    environment_name = f"gpu-teaching-cpu-smoke-ce-{suffix}"
    queue_name = f"gpu-teaching-cpu-smoke-queue-{suffix}"
    definition_name = f"gpu-teaching-cpu-smoke-job-{suffix}"
    job_id = None
    definition_arn = None
    environment_created = False
    queue_created = False
    account_id = boto3.client("sts", region_name=args.region).get_caller_identity()["Account"]
    batch = boto3.client("batch", region_name=args.region)
    instance_profile = f"arn:aws:iam::{account_id}:instance-profile/{args.instance_profile}"

    try:
        print(f"Creating CPU compute environment: {environment_name}")
        batch.create_compute_environment(
            computeEnvironmentName=environment_name,
            type="MANAGED",
            state="ENABLED",
            computeResources={
                "type": "EC2",
                "minvCpus": 0,
                "maxvCpus": 2,
                "instanceTypes": ["c6a.large"],
                "subnets": [VPC_SUBNET],
                "securityGroupIds": [SECURITY_GROUP],
                "instanceRole": instance_profile,
            },
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
            raise RuntimeError("CPU compute environment became INVALID")

        batch.create_job_queue(
            jobQueueName=queue_name,
            state="ENABLED",
            priority=1,
            computeEnvironmentOrder=[{"order": 1, "computeEnvironment": environment_name}],
        )
        queue_created = True
        wait_for(
            lambda: batch.describe_job_queues(jobQueues=[queue_name])["jobQueues"][0]["status"],
            {"VALID", "INVALID"},
            args.timeout,
            "Job queue",
        )

        definition = batch.register_job_definition(
            jobDefinitionName=definition_name,
            type="container",
            containerProperties={
                "image": "public.ecr.aws/docker/library/busybox:latest",
                "vcpus": 1,
                "memory": 128,
                "command": ["sh", "-c", "echo CPU Batch smoke test passed"],
            },
        )
        definition_arn = definition["jobDefinitionArn"]
        job_id = batch.submit_job(
            jobName=f"cpu-smoke-{suffix}", jobQueue=queue_name, jobDefinition=definition_arn
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
        print(f"CPU Batch smoke test failed: {error}", file=sys.stderr)
        sys.exit(1)