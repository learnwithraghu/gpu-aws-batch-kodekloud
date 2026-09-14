# helpers/

Utility scripts for pre-flight validation and course teardown.

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
python helpers/check_spot_availability.py \
  --vpc-id        vpc-xxxxxxxxxxxxxxxxx \
  --subnet-id     subnet-xxxxxxxxxxxxxxxxx \
  --security-group-id sg-xxxxxxxxxxxxxxxxx

# With optional overrides:
python helpers/check_spot_availability.py \
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
pip install boto3 python-dotenv
```

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
python helpers/teardown.py --dry-run

# Delete Batch resources only:
python helpers/teardown.py

# Delete everything:
python helpers/teardown.py --delete-ecr --delete-s3

# Different region:
python helpers/teardown.py --region us-east-1 --dry-run
```

### Prerequisites

```bash
pip install boto3 python-dotenv
```

AWS credentials must have:
- `batch:DescribeJobQueues`, `batch:UpdateJobQueue`, `batch:DeleteJobQueue`
- `batch:DescribeComputeEnvironments`, `batch:UpdateComputeEnvironment`, `batch:DeleteComputeEnvironment`
- `batch:DescribeJobDefinitions`, `batch:DeregisterJobDefinition`
- `ecr:DeleteRepository` (if using `--delete-ecr`)
- `s3:DeleteBucket`, `s3:DeleteObject`, `s3:ListBucket`, `s3:ListBucketVersions` (if using `--delete-s3`)
