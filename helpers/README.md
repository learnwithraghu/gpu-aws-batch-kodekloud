# helpers/

Utility scripts for pre-flight validation and course teardown.

---

## Setup

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if it is
not already available:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Open a new terminal, or reload your shell so `uv` is available. The commands
below use `uv run --with ...` to install the required Python packages in an
isolated environment on demand.

Install AWS CLI v2 if it is not already installed. Download and install it
outside this repository (e.g. in `/tmp`) so the installer files are never
accidentally committed:

```bash
cd /tmp
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws --version
cd -
```

Configure the AWS CLI before running either helper. The command prompts for
your access key ID and secret access key; enter them only at the prompt. Do
not put credentials in this repository or commit them to `.env` files.

```bash
aws configure
# AWS Access Key ID [None]: <enter your access key ID>
# AWS Secret Access Key [None]: <enter your secret access key>
# Default region name [None]: us-east-1
# Default output format [None]: json
```

Confirm that the configured credentials work:

```bash
aws sts get-caller-identity
```

The AWS CLI stores the default profile outside the repository in
`~/.aws/credentials` and `~/.aws/config`. Use it by running the helpers without
an `AWS_PROFILE` setting:

```bash
uv run --with boto3 --with python-dotenv python helpers/teardown.py --dry-run
```

To use a named profile, first create it with `aws configure --profile NAME`,
then replace `NAME` below with the actual profile name. Do not run this command
literally with `NAME`.

```bash
AWS_PROFILE=your-profile uv run --with boto3 --with python-dotenv python helpers/teardown.py --dry-run
```

---

## setup_infra.sh

Tutor helper to spin the course infrastructure up and down quickly.

```bash
# Create the S3 buckets (idempotent — existing buckets are skipped):
bash helpers/setup_infra.sh up

# Tear everything down (Batch, S3, ...; asks for confirmation):
bash helpers/setup_infra.sh down

# Tear down including the ECR repository:
bash helpers/setup_infra.sh down --delete-ecr

# Preview the teardown without deleting anything:
bash helpers/setup_infra.sh down --dry-run
```

`up` provisions two S3 buckets in your region via `create_buckets.sh`:

| Bucket | Purpose |
|--------|---------|
| `gpu-teaching-images-<account-id>` | Raw images, uploaded manually by the tutor |
| `gpu-teaching-captions-csv-<account-id>` | CSV files mapping each image to its caption |

Bucket names are suffixed with your AWS account ID so they never collide with
other accounts. The resolved names are written to `.env` as `S3_IMAGES_BUCKET`
and `S3_CSV_BUCKET` (with `S3_BUCKET` set to the images bucket for lesson
scripts). Re-running `up` detects existing buckets with `s3api head-bucket`
and skips them.

`down` delegates to `teardown.py`, which deletes both buckets when
`--delete-s3` is used.

---

## organize_uploads.sh

The Batch jobs caption everything under `images/<stem>/` in the images bucket,
but a tutor may drop images at the bucket root. This helper moves any
root-level image objects into `images/<stem>/` (default stem: `sample`):

```bash
bash helpers/organize_uploads.sh             # moves root-level images into images/sample/
bash helpers/organize_uploads.sh --stem demo # different batch folder
bash helpers/organize_uploads.sh --dry-run   # preview without moving
```

Then caption the batch with lesson 03 step 04 (`python main.py --batch-stem sample`).

---

## create_buckets.sh

Idempotent S3 bucket setup (invoked by `setup_infra.sh up`, also usable on
its own):

```bash
bash helpers/create_buckets.sh              # region from .env / AWS CLI default
bash helpers/create_buckets.sh --region us-east-1
```

Requires the AWS CLI to be configured (see Setup above) and permissions for
`s3:CreateBucket`, `s3:HeadBucket`, and `sts:GetCallerIdentity`.

---

## check_spot_availability.py

Pre-flight check before provisioning AWS Batch infrastructure. Verifies that
`g4dn.xlarge` (NVIDIA T4 — the most widely available GPU instance) capacity is
available in your target VPC/subnet/security-group, for **Spot, On-Demand, or
both**, so you don't waste time setting up Batch only to discover the instance
type isn't available in that AZ.

### What it checks

| Check | Applies to | What it does |
|-------|-----------|-------------|
| **Instance type offering** | Both | Confirms the instance type is offered in the target AZ |
| **Spot price history** | Spot | Current spot price vs on-demand, % savings |
| **Spot placement score** | Spot | AWS's 1–10 capacity confidence score (≥ 7 = healthy) |
| **Dry-run request** | Both | Confirms subnet/SG combo is valid and IAM permissions allow the launch (`RequestSpotInstances` for Spot, `RunInstances` for On-Demand) |

### Usage

```bash
# Check both Spot and On-Demand (default):
uv run --with boto3 --with python-dotenv python helpers/check_spot_availability.py

# Check only Spot:
uv run --with boto3 --with python-dotenv python helpers/check_spot_availability.py --capacity-type spot

# Check only On-Demand:
uv run --with boto3 --with python-dotenv python helpers/check_spot_availability.py --capacity-type on-demand

# The fixed course network values used by default:
# VPC: vpc-3f0b1a58
# Subnet: subnet-b560b3fd
# Security group: sg-bd00e4f5
```

### Exit codes

| Code | Meaning |
|------|---------|
| `0` | ✅ GOOD — safe to provision |
| `1` | ❌ UNAVAILABLE — spot request rejected (check IAM/network) |
| `2` | ⚠️ MARGINAL — capacity limited, consider different AZ or instance type |

### Prerequisites

```bash
uv run --with boto3 --with python-dotenv python helpers/check_spot_availability.py --help
```

Complete the shared AWS CLI setup above before running this command.

AWS credentials must have:
- `ec2:DescribeInstanceTypeOfferings`
- `ec2:DescribeSpotPriceHistory`
- `ec2:GetSpotPlacementScores`
- `ec2:RequestSpotInstances` (for Spot dry-run — no instance is actually launched)
- `ec2:RunInstances` (for On-Demand dry-run — no instance is actually launched)
- `ec2:DescribeSubnets`
- `pricing:GetProducts` (optional — used for on-demand price comparison)

---

## Batch Smoke Tests

These tests validate that AWS Batch can schedule and run a real container.
They use **persistent, reusable** Batch resources: on the first run each test
creates its compute environment, job queue, and job definition with stable
names; every later run reuses them (re-creating only what is missing) and
deletes nothing. This skips the create/wait/delete cycle so repeat runs are
much faster. The compute environments use `minvCpus: 0`, so no compute
capacity is left running or billed between runs.

### Run everything in order

`run_smoke_tests.sh` runs all smoke tests in order: spot pre-flight, GPU spot,
GPU on-demand, then CPU. It stops at the first failed stage unless
`--continue-on-failure` is passed.

```bash
bash helpers/run_smoke_tests.sh

# Skip the spot availability pre-flight check:
bash helpers/run_smoke_tests.sh --skip-preflight

# Run every stage even if an earlier one fails:
bash helpers/run_smoke_tests.sh --continue-on-failure
```

### Persistent resource names

| Resource | Name |
|----------|------|
| GPU Spot compute environment | `gpu-teaching-gpu-smoke-ce-spot` |
| GPU Spot job queue | `gpu-teaching-gpu-smoke-queue-spot` |
| GPU On-Demand compute environment | `gpu-teaching-gpu-smoke-ce-on-demand` |
| GPU On-Demand job queue | `gpu-teaching-gpu-smoke-queue-on-demand` |
| GPU job definition | `gpu-teaching-gpu-smoke-job` |
| CPU compute environment | `gpu-teaching-cpu-smoke-ce` |
| CPU job queue | `gpu-teaching-cpu-smoke-queue` |
| CPU job definition | `gpu-teaching-cpu-smoke-job` |

If one of these exists but is `INVALID` or points at the wrong compute
environment, the test fails with a message telling you to fix or remove it
manually — the scripts never delete anything.

> **Note**: `teardown.py` matches the `gpu-teaching-*` prefix, so it removes
> these persistent smoke resources too. That is intentional — teardown is the
> "done with the course, wipe it all" step. If you run it, the next smoke test
> simply re-creates what it needs.

### CPU-only test

```bash
uv run --with boto3 --with python-dotenv python helpers/test_cpu_batch.py
```

This requires an EC2 instance profile named `ecsInstanceRole`, as used by the
course Batch setup. Supply a different profile name with `--instance-profile`.
The VPC subnet and security group are the fixed course values.

### GPU test

The GPU test uses `g4dn.xlarge` (NVIDIA T4) and runs `nvidia-smi` in a CUDA
container. It can incur GPU instance charges while a job runs. By default it
tests an **on-demand** compute environment; pass `--capacity-type spot` to
test a Spot compute environment instead. Run:

```bash
# On-demand (default):
uv run --with boto3 --with python-dotenv python helpers/test_gpu_batch.py

# Spot:
uv run --with boto3 --with python-dotenv python helpers/test_gpu_batch.py --capacity-type spot
```

Its container command runs `nvidia-smi`, so a successful job confirms that
Batch can provision a GPU instance (Spot or On-Demand) and the scheduled
container can access it. If a GPU instance is not provisioned within 3
minutes, the job is terminated (the persistent resources are kept).

The tests require `batch:CreateComputeEnvironment`, `batch:CreateJobQueue`,
`batch:RegisterJobDefinition`, `batch:SubmitJob`, `batch:Describe*`,
`batch:UpdateComputeEnvironment`, `batch:UpdateJobQueue`, and
`batch:TerminateJob`. The CPU test also requires `sts:GetCallerIdentity`.

---

## teardown.py

Safely removes all AWS resources created by the GPU Teaching course, in the
correct order (Batch enforces dependency ordering on deletion).

### What it deletes

| Step | Resource | Flag |
|------|----------|------|
| 1 | Job Queues matching `gpu-teaching-*` | always |
| 2 | Compute Environments matching `gpu-teaching-*` | always |
| 3 | Job Definition revisions for `gpu-teaching-job-def` | always |
| 4 | ECR repository `gpu-teaching` + all images | `--delete-ecr` |
| 5 | S3 bucket (from `S3_BUCKET` in `.env`) | `--delete-s3` |

### Usage

```bash
# See what would be deleted (safe to run anytime):
uv run --with boto3 --with python-dotenv python helpers/teardown.py --dry-run

# Delete Batch resources only:
uv run --with boto3 --with python-dotenv python helpers/teardown.py

# Delete everything:
uv run --with boto3 --with python-dotenv python helpers/teardown.py --delete-ecr --delete-s3

# Different region:
uv run --with boto3 --with python-dotenv python helpers/teardown.py --region us-east-1 --dry-run
```

### Prerequisites

```bash
uv run --with boto3 --with python-dotenv python helpers/teardown.py --help
```

Complete the shared AWS CLI setup above before running this command.

AWS credentials must have:
- `batch:DescribeJobQueues`, `batch:UpdateJobQueue`, `batch:DeleteJobQueue`
- `batch:DescribeComputeEnvironments`, `batch:UpdateComputeEnvironment`, `batch:DeleteComputeEnvironment`
- `batch:DescribeJobDefinitions`, `batch:DeregisterJobDefinition`
- `ecr:DeleteRepository` (if using `--delete-ecr`)
- `s3:DeleteBucket`, `s3:DeleteObject`, `s3:ListBucket`, `s3:ListBucketVersions` (if using `--delete-s3`)

