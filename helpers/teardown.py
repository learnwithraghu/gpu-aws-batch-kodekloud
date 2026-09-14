#!/usr/bin/env python3
"""
helpers/teardown.py

Tear down all AWS resources created by the GPU Teaching course.

Respects AWS Batch deletion ordering:
  1. Disable & delete Job Queues    (must be disabled before deletion)
  2. Disable & delete Compute Environments  (queues must be deleted first)
  3. Deregister Job Definitions
  4. (optional) Delete ECR repository + all images
  5. (optional) Empty & delete S3 bucket

Usage:
  # Dry run (see what would be deleted, do nothing):
  python helpers/teardown.py --dry-run

  # Delete Batch resources only:
  python helpers/teardown.py

  # Delete everything including ECR and S3:
  python helpers/teardown.py --delete-ecr --delete-s3

  # Different region:
  python helpers/teardown.py --region us-east-1
"""

import argparse
import os
import sys
import time

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# ── colour helpers ────────────────────────────────────────────────────────────
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def done(msg: str) -> str:  return f"{GREEN}✅ {msg}{RESET}"
def skip(msg: str) -> str:  return f"{YELLOW}⏭  {msg}{RESET}"
def fail(msg: str) -> str:  return f"{RED}❌ {msg}{RESET}"
def hdr(msg: str)  -> str:  return f"\n{BOLD}{msg}{RESET}"
def dry(msg: str)  -> str:  return f"{YELLOW}[DRY RUN] {msg}{RESET}"


# ── helpers ───────────────────────────────────────────────────────────────────
def poll_until(describe_fn, name: str, desired_state: str, interval: int = 10, timeout: int = 300):
    """
    Poll describe_fn() until the resource reaches desired_state.
    describe_fn must return a status string.
    """
    elapsed = 0
    while elapsed < timeout:
        state = describe_fn()
        print(f"  {name}: {state} (waiting for {desired_state}…)", end="\r")
        if state == desired_state:
            print(f"  {name}: {state}           ")  # clear trailing chars
            return
        time.sleep(interval)
        elapsed += interval
    raise TimeoutError(f"{name} did not reach {desired_state} within {timeout}s")


# ── Step 1 + 2: Job Queues ────────────────────────────────────────────────────
def teardown_job_queues(batch, dry_run: bool) -> list[str]:
    """Disable and delete all gpu-teaching-* job queues. Returns queue ARNs deleted."""
    print(hdr("[1/5] Job Queues"))

    resp = batch.describe_job_queues()
    queues = [q for q in resp["jobQueues"] if "gpu-teaching" in q["jobQueueName"]]

    if not queues:
        print(skip("No gpu-teaching job queues found"))
        return []

    deleted = []
    for q in queues:
        name = q["jobQueueName"]
        state = q["state"]

        if dry_run:
            print(dry(f"Would disable + delete job queue: {name}  (currently {state})"))
            continue

        # Disable first (required before deletion)
        if state != "DISABLED":
            print(f"  Disabling {name}…")
            batch.update_job_queue(jobQueue=name, state="DISABLED")
            poll_until(
                lambda n=name: batch.describe_job_queues(jobQueues=[n])["jobQueues"][0]["state"],
                name, "DISABLED"
            )

        print(f"  Deleting {name}…")
        batch.delete_job_queue(jobQueue=name)
        print(done(f"Deleted job queue: {name}"))
        deleted.append(name)

    return deleted


# ── Step 3: Compute Environments ──────────────────────────────────────────────
def teardown_compute_envs(batch, dry_run: bool) -> list[str]:
    """Disable and delete all gpu-teaching-* compute environments."""
    print(hdr("[2/5] Compute Environments"))

    resp = batch.describe_compute_environments()
    envs = [e for e in resp["computeEnvironments"] if "gpu-teaching" in e["computeEnvironmentName"]]

    if not envs:
        print(skip("No gpu-teaching compute environments found"))
        return []

    deleted = []
    for e in envs:
        name  = e["computeEnvironmentName"]
        state = e["state"]

        if dry_run:
            print(dry(f"Would disable + delete compute environment: {name}  (currently {state})"))
            continue

        # Must be DISABLED before deletion
        if state != "DISABLED":
            print(f"  Disabling {name}…")
            batch.update_compute_environment(computeEnvironment=name, state="DISABLED")

        # Poll until DISABLED and also VALID (status, not state)
        def ce_status(n=name):
            info = batch.describe_compute_environments(computeEnvironments=[n])["computeEnvironments"][0]
            return f"{info['state']}/{info['status']}"

        poll_until(
            lambda n=name: batch.describe_compute_environments(
                computeEnvironments=[n])["computeEnvironments"][0]["state"],
            name, "DISABLED"
        )

        print(f"  Deleting {name}…")
        batch.delete_compute_environment(computeEnvironment=name)
        print(done(f"Deleted compute environment: {name}"))
        deleted.append(name)

    return deleted


# ── Step 4: Job Definitions ───────────────────────────────────────────────────
def teardown_job_definitions(batch, dry_run: bool) -> int:
    """Deregister all revisions of gpu-teaching-* job definitions."""
    print(hdr("[3/5] Job Definitions"))

    resp = batch.describe_job_definitions(status="ACTIVE")
    defs = [
        d for d in resp["jobDefinitions"]
        if "gpu-teaching" in d["jobDefinitionName"]
    ]

    if not defs:
        print(skip("No active gpu-teaching job definitions found"))
        return 0

    count = 0
    for d in defs:
        arn = d["jobDefinitionArn"]
        name_rev = f"{d['jobDefinitionName']}:{d['revision']}"

        if dry_run:
            print(dry(f"Would deregister job definition: {name_rev}"))
            continue

        batch.deregister_job_definition(jobDefinition=arn)
        print(done(f"Deregistered: {name_rev}"))
        count += 1

    return count


# ── Step 5 (optional): ECR repository ────────────────────────────────────────
def teardown_ecr(region: str, dry_run: bool) -> bool:
    """Force-delete the gpu-teaching ECR repository and all its images."""
    print(hdr("[4/5] ECR Repository"))

    ecr = boto3.client("ecr", region_name=region)

    try:
        ecr.describe_repositories(repositoryNames=["gpu-teaching"])
    except ClientError as e:
        if e.response["Error"]["Code"] == "RepositoryNotFoundException":
            print(skip("ECR repository gpu-teaching not found — already deleted?"))
            return False
        raise

    if dry_run:
        print(dry("Would delete ECR repository: gpu-teaching (and all images)"))
        return False

    ecr.delete_repository(repositoryName="gpu-teaching", force=True)
    print(done("Deleted ECR repository: gpu-teaching (all images removed)"))
    return True


# ── Step 6 (optional): S3 bucket ─────────────────────────────────────────────
def teardown_s3(bucket: str, dry_run: bool) -> bool:
    """Empty and delete the S3 bucket."""
    print(hdr("[5/5] S3 Bucket"))

    if not bucket:
        print(skip("S3_BUCKET not set in .env — skipping"))
        return False

    s3 = boto3.resource("s3")
    bucket_obj = s3.Bucket(bucket)

    # Check the bucket exists
    try:
        boto3.client("s3").head_bucket(Bucket=bucket)
    except ClientError as e:
        code = e.response["Error"]["Code"]
        if code in ("404", "NoSuchBucket"):
            print(skip(f"S3 bucket {bucket} not found — already deleted?"))
            return False
        raise

    if dry_run:
        # Count objects without deleting
        count = sum(1 for _ in bucket_obj.objects.all())
        print(dry(f"Would delete S3 bucket: {bucket}  ({count} objects)"))
        return False

    # Delete all object versions (handles versioned buckets too)
    print(f"  Emptying {bucket}…")
    bucket_obj.object_versions.delete()
    bucket_obj.objects.delete()

    boto3.client("s3").delete_bucket(Bucket=bucket)
    print(done(f"Deleted S3 bucket: {bucket}"))
    return True


# ── main ──────────────────────────────────────────────────────────────────────
def main():
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    load_dotenv(env_path)

    parser = argparse.ArgumentParser(
        description="Tear down all AWS GPU Teaching course resources.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--region",     default=os.environ.get("AWS_DEFAULT_REGION", "ap-northeast-1"),
                        help="AWS region (default: ap-northeast-1 or AWS_DEFAULT_REGION from .env)")
    parser.add_argument("--delete-ecr", action="store_true",
                        help="Also delete the ECR repository and all images")
    parser.add_argument("--delete-s3",  action="store_true",
                        help="Also empty and delete the S3 bucket (uses S3_BUCKET from .env)")
    parser.add_argument("--dry-run",    action="store_true",
                        help="Print what would be deleted; do not actually delete anything")
    args = parser.parse_args()

    s3_bucket = os.environ.get("S3_BUCKET", "")

    print(f"\n{BOLD}=== GPU Teaching Teardown ==={RESET}")
    if args.dry_run:
        print(f"{YELLOW}DRY RUN — no resources will be deleted{RESET}")
    print(f"  Region     : {args.region}")
    print(f"  Delete ECR : {args.delete_ecr}")
    print(f"  Delete S3  : {args.delete_s3}  (bucket: {s3_bucket or '(not set)'})")

    if not args.dry_run:
        confirm = input("\n⚠️  This will permanently delete AWS resources. Type 'yes' to continue: ")
        if confirm.strip().lower() != "yes":
            print("Aborted.")
            sys.exit(0)

    batch = boto3.client("batch", region_name=args.region)

    # Track what was deleted for the summary
    deleted_queues = teardown_job_queues(batch, args.dry_run)
    deleted_envs   = teardown_compute_envs(batch, args.dry_run)
    deleted_defs   = teardown_job_definitions(batch, args.dry_run)

    ecr_deleted = False
    if args.delete_ecr:
        ecr_deleted = teardown_ecr(args.region, args.dry_run)
    else:
        print(hdr("[4/5] ECR Repository"))
        print(skip("Skipped (pass --delete-ecr to include)"))

    s3_deleted = False
    if args.delete_s3:
        s3_deleted = teardown_s3(s3_bucket, args.dry_run)
    else:
        print(hdr("[5/5] S3 Bucket"))
        print(skip("Skipped (pass --delete-s3 to include)"))

    # ── Summary ───────────────────────────────────────────────────────────────
    print(hdr("=== Teardown Summary ==="))
    if args.dry_run:
        print(f"{YELLOW}  (DRY RUN — nothing was actually deleted){RESET}")
    else:
        print(f"  Job queues deleted         : {len(deleted_queues)}")
        print(f"  Compute envs deleted       : {len(deleted_envs)}")
        print(f"  Job definitions deregistered: {deleted_defs}")
        print(f"  ECR repository deleted     : {'yes' if ecr_deleted else 'no'}")
        print(f"  S3 bucket deleted          : {'yes' if s3_deleted else 'no'}")
        print(f"\n{done('Teardown complete.')}")


if __name__ == "__main__":
    main()
