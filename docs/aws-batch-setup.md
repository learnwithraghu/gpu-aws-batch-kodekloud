# AWS Batch setup (live inventory)

Source of truth for the course AWS account. Gathered from the AWS CLI on
2026-09-27. Use this instead of re-discovering queues, job definitions,
buckets, and network IDs every session.

Account-specific values (account ID, bucket suffixes, ECR registry) live in
the local gitignored `.env` — resolve them with
`aws sts get-caller-identity` or copy from `.env.example` on the machine
that owns the account. **Do not commit account IDs, ARNs, or credentials.**

Credentials live outside the repo (`aws configure` → `~/.aws/`). Never put
keys in `.env` or commit them.

To refresh this file after infra changes, see [Refresh the inventory](#refresh-the-inventory).

---

## Account and region

| Item | Value |
|------|--------|
| Account | from `aws sts get-caller-identity` — keep out of git |
| IAM user (CLI) | the configured default-profile user |
| CLI identity | local submit/describe/S3 from the laptop |
| Region | **`ap-northeast-1`** (Tokyo) |
| Default CLI profile | default (`aws configure`, no `AWS_PROFILE` needed) |

Lesson scripts and helpers read `.env` at the repo root. Copy from
`.env.example` if `.env` is missing. Typical keys (values are local):

```
AWS_DEFAULT_REGION=ap-northeast-1
S3_BUCKET=gpu-teaching-images-<account-id>
S3_IMAGES_BUCKET=gpu-teaching-images-<account-id>
S3_CSV_BUCKET=gpu-teaching-captions-csv-<account-id>
BATCH_JOB_QUEUE=gpu-teaching-gpu-smoke-queue-spot
BATCH_JOB_DEFINITION=gpu-teaching-caption-job
ECR_IMAGE_URI=<account-id>.dkr.ecr.ap-northeast-1.amazonaws.com/gpu-teaching:latest
```

---

## What to use when developing lessons

These are the names the lesson CLI commands already expect via `.env`.

| Role | Name | Notes |
|------|------|--------|
| Default job queue | `gpu-teaching-gpu-smoke-queue-spot` | GPU Spot (`g4dn.xlarge`) |
| Fallback job queue | `gpu-teaching-gpu-smoke-queue-on-demand` | If a job sits in `RUNNABLE` (no Spot capacity) |
| Lesson job definition | `gpu-teaching-caption-job` | Use revision **`:4` or later** (12288 MiB + job role + explicit awslogs). `:1` is broken (16 GiB). `:2` has no `jobRoleArn`. |
| Image | `<account-id>.dkr.ecr.ap-northeast-1.amazonaws.com/gpu-teaching:latest` | Course CUDA + PyTorch + BLIP image |
| Images bucket | `gpu-teaching-images-<account-id>` | Input: `images/<stem>/…` |
| Catalog bucket | `gpu-teaching-captions-csv-<account-id>` | Output: `descriptions/<stem>/descriptions.csv` |
| Logs | CloudWatch `/aws/batch/job` | Stream name looks like `gpu-teaching-caption-job/default/<taskId>` |

Do **not** create `gpu-teaching-ce`, `gpu-teaching-queue`, or
`gpu-teaching-job-def`. Those names appear in the README one-time-setup
example only. Live resources use the `gpu-teaching-*-smoke-*` names plus
`gpu-teaching-caption-job`.

---

## Compute environments

All three are `MANAGED`, `ENABLED`, `VALID`, ECS orchestration, `minvCpus: 0`
(no idle instances billed). Shared network and instance profile:

- Subnet: `subnet-b560b3fd`
- Security group: `sg-bd00e4f5`
- Instance profile: `ecsInstanceRole`
- Service role: `AWSServiceRoleForBatch` (Batch service-linked role)

### GPU Spot — default for lessons

| Field | Value |
|-------|--------|
| Name | `gpu-teaching-gpu-smoke-ce-spot` |
| Type | `SPOT` |
| Allocation | `SPOT_CAPACITY_OPTIMIZED` |
| Instance | `g4dn.xlarge` (NVIDIA T4, 4 vCPU, 16 GiB) |
| vCPUs | min 0 / max 4 / desired 0 |
| AMI | `ECS_AL2023_NVIDIA` |
| ECS cluster | `AWSBatch-gpu-teaching-gpu-smoke-ce-spot-*` (Batch-managed) |
| Queue | `gpu-teaching-gpu-smoke-queue-spot` (priority 1) |

Quota: **All G and VT Spot Instance Requests = 8 vCPUs** in
`ap-northeast-1`. This CE caps at 4, so one GPU Spot instance at a time.

### GPU On-Demand — fallback

| Field | Value |
|-------|--------|
| Name | `gpu-teaching-gpu-smoke-ce-on-demand` |
| Type | `EC2` (on-demand) |
| Instance | `g4dn.xlarge` |
| vCPUs | min 0 / max 4 / desired 0 |
| AMI | `ECS_AL2023_NVIDIA` |
| Queue | `gpu-teaching-gpu-smoke-queue-on-demand` |

Set `BATCH_JOB_QUEUE=gpu-teaching-gpu-smoke-queue-on-demand` in `.env` when
Spot will not place.

### CPU — smoke tests only

| Field | Value |
|-------|--------|
| Name | `gpu-teaching-cpu-smoke-ce` |
| Type | `EC2` |
| Instance | `c6a.large` |
| vCPUs | min 0 / max 2 / desired 0 |
| AMI | `ECS_AL2023` |
| Queue | `gpu-teaching-cpu-smoke-queue` |
| Job definition | `gpu-teaching-cpu-smoke-job` (busybox echo) |

---

## Job definitions

Submit by **name**; Batch uses the latest ACTIVE revision unless you pin one.

### `gpu-teaching-caption-job` — food catalog job

Use **revision 4** (or a newer matching revision with `logConfiguration`). Do not submit `:1` or `:2`.

| Field | Revision 4+ (good) | Revision 3 | Revision 2 | Revision 1 (broken) |
|-------|--------------------|------------|------------|---------------------|
| Image | `…/gpu-teaching:latest` | same | same | same |
| VCPU | 4 | 4 | 4 | 4 |
| MEMORY | **12288 MiB** | 12288 MiB | 12288 MiB | 16384 MiB — never placeable |
| GPU | 1 | 1 | 1 | 1 |
| `jobRoleArn` | `gpu-teaching-batch-job-role` | same | none — S3 `AccessDenied` | none |
| Env | `S3_BUCKET`, `S3_CSV_BUCKET`, `PYTHONUNBUFFERED=1` | buckets only | same | same |
| Logs | `awslogs` → `/aws/batch/job` | often default awslogs | — | — |
| Default command | `python -c "import torch; print(…)"` | same | same | same |

Lesson 08 `aws batch submit-job` overrides `command` to `python /app/describe_items.py` and passes
`IMAGE_PREFIX`, `BATCH_SIZE`, and the two bucket env vars.

**Memory rule:** ECS on `g4dn.xlarge` does not register the full 16 GiB
(OS + agent). Asking for `16384` yields
`MISCONFIGURATION:JOB_RESOURCE_REQUIREMENT` and the job never leaves
`RUNNABLE`. Keep MEMORY at **12288**.

**Logging:** Ensure the group exists once:

```bash
aws logs create-log-group --log-group-name /aws/batch/job --region ap-northeast-1 2>/dev/null || true
```

Streams appear only after `STARTING` / `RUNNING`. `RUNNABLE` has no container and no app logs.

Re-register when the image, memory, GPU, job role, or logging config is wrong (lesson 07).
Every `register-job-definition` call creates a new revision.

### `gpu-teaching-gpu-smoke-job` — GPU smoke only

Latest revision **7**. Image `nvidia/cuda:12.6.3-runtime-ubuntu22.04`,
1 vCPU, 1024 MiB, 1 GPU, command `nvidia-smi && echo GPU Batch smoke test passed`.
Created/reused by `helpers/test_gpu_batch.py`. Not for lessons.

---

## Container image (ECR)

| Field | Value |
|-------|--------|
| Repository | `gpu-teaching` |
| URI | `<account-id>.dkr.ecr.ap-northeast-1.amazonaws.com/gpu-teaching:latest` |
| Tag mutability | MUTABLE |
| Scan on push | on |
| Size | ~3.8 GB |
| Last push | 2026-09-28 |
| Last pull | 2026-09-28 |

Dockerfile (repo root): `pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime`,
`transformers==4.46.3`, Pillow, boto3, python-dotenv. Lesson 02's
`photos.py` and `describe_items.py` are copied to `/app/`. Batch runs
`python /app/describe_items.py`, which imports `photos.py`. Batch runs only what is
**baked into this image**.

After any change to `Dockerfile` or `lessons/02-the-container-program/`, rebuild and push (lessons 03 and 04):

```bash
bash helpers/push_ecr_image.sh
```

The job definition URI stays `:latest`; new jobs pull the new image.
`:latest` was pushed on 2026-09-28 with `/app/describe_items.py`.

---

## S3 layout

| Bucket | Purpose | Current objects (2026-09-27) |
|--------|---------|------------------------------|
| `gpu-teaching-images-<account-id>` | Raw images | `images/sample/` (one sample PNG) |
| `gpu-teaching-captions-csv-<account-id>` | Food catalog CSVs | `descriptions/<stem>/descriptions.csv` |

```
s3://gpu-teaching-images-<account-id>/images/<stem>/…     # vendor food photos
s3://gpu-teaching-captions-csv-<account-id>/descriptions/<stem>/descriptions.csv
```

`S3_BUCKET` is the images bucket. The CSV bucket name still says `captions`
because that is the live bucket; new files use the `descriptions/` prefix.

Create buckets with the CLI in lesson 05. Tutor shortcut: `bash helpers/setup_infra.sh up`

---

## Network

Default VPC in Tokyo. Instances get a public IP (`MapPublicIpOnLaunch=true`)
so they can pull ECR and download the BLIP model from Hugging Face.

| Resource | ID | Detail |
|----------|-----|--------|
| VPC | `vpc-3f0b1a58` | default, `172.31.0.0/16` |
| Subnet | `subnet-b560b3fd` | `ap-northeast-1a` / `apne1-az4`, `172.31.32.0/20` |
| Security group | `sg-bd00e4f5` | default SG; egress `0.0.0.0/0` |

Hard-coded in `helpers/test_cpu_batch.py` and
`helpers/check_spot_availability.py`. Do not change unless you recreate the
compute environments.

---

## IAM

| Principal | Name | Used for |
|-----------|------|----------|
| Batch service-linked role | `AWSServiceRoleForBatch` | Batch manages CEs, ECS clusters, scaling |
| EC2 instance role + profile | `ecsInstanceRole` | ECS agent, ECR pull, CloudWatch logs (`AmazonEC2ContainerServiceforEC2Role`) |
| Batch job role | `gpu-teaching-batch-job-role` | Container S3 access (`jobRoleArn` on caption job def `:3`+) |
| Local CLI user | configured default profile | Submit jobs, S3 upload, register job defs |

`ecsInstanceRole` has no S3. Caption containers assume
`gpu-teaching-batch-job-role` (`BATCH_JOB_ROLE_ARN` in `.env`): `ListBucket`
on both course buckets, `GetObject` on the images bucket, `GetObject` and
`PutObject` on the descriptions bucket. Laptop-side scripts still use the CLI
user. The README example name `BatchJobRole` is not a live resource.

---

## How a job is submitted

Lesson 08 runs `aws batch submit-job` with `python /app/describe_items.py` and
polls `aws batch describe-jobs` until `SUCCEEDED` or `FAILED`.

| Variable | Meaning |
|----------|---------|
| `S3_BUCKET` | Images bucket |
| `S3_CSV_BUCKET` | Descriptions CSV bucket |
| `IMAGE_PREFIX` | e.g. `images/vendor-a` |
| `BATCH_SIZE` | Images per GPU forward pass (default 8) |

---

## Debug cheatsheet

```bash
# Job status + why it stopped
aws batch describe-jobs --jobs <job-id> --region ap-northeast-1 \
  --query 'jobs[0].[status,statusReason,attempts[0].container.exitCode,attempts[0].container.logStreamName]'

# Container logs
aws logs get-log-events --log-group-name /aws/batch/job \
  --log-stream-name 'gpu-teaching-caption-job/default/<taskId>' \
  --region ap-northeast-1

# Queue / CE health
aws batch describe-job-queues --job-queues gpu-teaching-gpu-smoke-queue-spot --region ap-northeast-1
aws batch describe-compute-environments --compute-environments gpu-teaching-gpu-smoke-ce-spot --region ap-northeast-1
```

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| `MISCONFIGURATION:JOB_RESOURCE_REQUIREMENT` | Job asked for 16 GiB | Use `gpu-teaching-caption-job:4` (12288 MiB) |
| Stuck `RUNNABLE` | No Spot capacity / quota | Switch `.env` to `gpu-teaching-gpu-smoke-queue-on-demand` |
| Exit 1, transformers / PyTorch error | Image predates the 4.46.3 pin | `bash helpers/push_ecr_image.sh` then resubmit |
| Exit 1, old caption script missing | Image still has `/app/lessons/` | `bash helpers/push_ecr_image.sh` so `/app/describe_items.py` is in ECR |
| Exit 1, S3 `AccessDenied` | Job def older than `:3`, or role policy missing the bucket | Re-register (lesson 07) so `jobRoleArn` is `gpu-teaching-batch-job-role` |
| Smoke test provision timeout (3 min) | GPU instance not launched in time | Persistent CEs stay; retry or use on-demand |

Cost: `g4dn.xlarge` Spot in Tokyo is roughly $0.16–0.24/hr. A 2–5 minute
lesson job is a few cents. `minvCpus=0` means no charge between jobs.

---

## Helpers that own this infra

| Script | What it does |
|--------|----------------|
| `helpers/setup_infra.sh up` | Create the two S3 buckets (idempotent) |
| `helpers/push_ecr_image.sh` | Build + push `gpu-teaching:latest` |
| `helpers/check_spot_availability.py` | Pre-flight for `g4dn.xlarge` in this VPC/subnet/SG |
| `helpers/test_gpu_batch.py` | Create/reuse GPU CE + queue + smoke job def |
| `helpers/test_cpu_batch.py` | Same for CPU |
| `helpers/run_smoke_tests.sh` | Spot pre-flight → GPU spot → GPU on-demand → CPU |
| `helpers/teardown.py` | Deletes all `gpu-teaching-*` Batch resources (and optionally ECR/S3) |

Smoke tests **reuse** these resources; they never delete them. Teardown
matches the `gpu-teaching-*` prefix and will wipe lesson queues too.

---

## Refresh the inventory

Re-run when someone recreates a CE, registers a new job-def revision, or
changes buckets. Then update the tables above. Resolve bucket names from
`.env` — do not paste account IDs into this file.

```bash
aws sts get-caller-identity
aws batch describe-compute-environments --region ap-northeast-1 \
  --query 'computeEnvironments[].{name:computeEnvironmentName,state:state,status:status,type:computeResources.type,instances:computeResources.instanceTypes,min:computeResources.minvCpus,max:computeResources.maxvCpus}'
aws batch describe-job-queues --region ap-northeast-1 \
  --query 'jobQueues[].{name:jobQueueName,state:state,ce:computeEnvironmentOrder[0].computeEnvironment}'
aws batch describe-job-definitions --status ACTIVE --region ap-northeast-1 \
  --query 'jobDefinitions[].{name:jobDefinitionName,rev:revision,image:containerProperties.image,req:containerProperties.resourceRequirements}'
aws ecr describe-images --repository-name gpu-teaching --region ap-northeast-1
aws s3 ls "s3://${S3_IMAGES_BUCKET}" --recursive
aws s3 ls "s3://${S3_CSV_BUCKET}" --recursive
```
