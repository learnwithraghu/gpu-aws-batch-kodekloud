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

Install AWS CLI v2 if it is not already installed:

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws --version
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

The AWS CLI stores this profile outside the repository in `~/.aws/credentials`
and `~/.aws/config`. To use a named profile, run `aws configure --profile NAME`
then set `AWS_PROFILE=NAME` before running a helper.

```bash
AWS_PROFILE=NAME uv run --with boto3 --with python-dotenv python helpers/teardown.py --dry-run
```

---

## check_spot_availability.py

Pre-flight check before provisioning AWS Batch infrastructure. Verifies that
`g4dn.xlarge` (or any GPU instance type) spot capacity is available in your
target VPC/subnet/security-group, so you don't waste time setting up Batch
only to discover spot instances aren't available in that AZ.

### What it checks

| Check | What it does |
|-------|-------------|
| **Spot price history** | Current spot price vs on-demand, % savings |
| **Spot placement score** | AWS's 1–10 capacity confidence score (≥ 7 = healthy) |
| **Dry-run spot request** | Confirms subnet/SG combo is valid and IAM permissions allow spot requests |

### Usage

```bash
uv run --with boto3 --with python-dotenv python helpers/check_spot_availability.py \
  --vpc-id        vpc-xxxxxxxxxxxxxxxxx \
  --subnet-id     subnet-xxxxxxxxxxxxxxxxx \
  --security-group-id sg-xxxxxxxxxxxxxxxxx

# With optional overrides:
uv run --with boto3 --with python-dotenv python helpers/check_spot_availability.py \
  --vpc-id        vpc-xxxxxxxxxxxxxxxxx \
  --subnet-id     subnet-xxxxxxxxxxxxxxxxx \
  --security-group-id sg-xxxxxxxxxxxxxxxxx \
  --instance-type g4dn.2xlarge \
  --region        ap-northeast-1
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
- `ec2:DescribeSpotPriceHistory`
- `ec2:GetSpotPlacementScores`
- `ec2:RequestSpotInstances` (for dry-run — no instance is actually launched)
- `ec2:DescribeSubnets`
- `pricing:GetProducts` (optional — used for on-demand price comparison)

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
