# 🖼️ GPU Teaching — Image → Caption Pipeline on AWS Batch

A hands-on 6-lesson course teaching GPUs to Data Scientists, using AWS Batch with GPU instances.

**What you'll build:** A pipeline that takes a folder of images, generates a natural-language caption for each one on a GPU with BLIP, and stores the results in S3 — a caption file pairing every image's S3 location with its caption.

---

## 🔔 AWS Quota Notes

| Region | Quota | Approved Limit | Date |
|--------|-------|----------------|------|
| ap-northeast-1 (Tokyo) | All G and VT Spot Instance Requests | **8 vCPUs** | 2026-09-13 |

If you need more than 8 vCPUs, request an increase via the [Service Quotas console](https://console.aws.amazon.com/servicequotas/home/services/ec2/quotas).

---

## 📚 Lessons

| # | Title | What you learn | AWS needed |
|---|-------|----------------|-----------|
| [00](lessons/00-docker-build/) | Docker Build & Push | Docker layers, ECR, CUDA base images | ECR |
| [01](lessons/01-why-gpu/) | Why GPU? | CPU vs GPU mental model | — |
| [02](lessons/02-first-batch-job/) | First Batch Job | AWS Batch concepts | Batch, ECR |
| [03](lessons/03-images-to-captions/) | Images → Captions | BLIP image captioning, S3 I/O | Batch, S3 |
| [04](lessons/04-full-pipeline/) | Full Pipeline | Job dependencies / DAG | Batch, S3 |
| [05](lessons/05-scale-and-cost/) | Scale & Cost | Array jobs, spot pricing | Batch, S3 |

Each lesson is **fully self-contained** — you can do them in order or jump to any one independently.

---

## 🔑 One-Time Setup

Do this once before starting any lesson.

### 1. Clone & configure secrets

```bash
git clone <this-repo>
cd gpu-teaching
cp .env.example .env
# Now edit .env and fill in your bucket name + image URI
```

### 2. Create an S3 bucket

```bash
aws s3 mb s3://your-gpu-teaching-bucket --region ap-northeast-1
```

Update `S3_BUCKET` in your `.env`.

### 3. Build & push the Docker image

```bash
# Authenticate Docker with ECR
aws ecr get-login-password --region ap-northeast-1 \
  | docker login --username AWS --password-stdin \
    $(aws sts get-caller-identity --query Account --output text).dkr.ecr.ap-northeast-1.amazonaws.com

# Create ECR repository
aws ecr create-repository --repository-name gpu-teaching --region ap-northeast-1

# Build and push
docker build -t gpu-teaching .
docker tag gpu-teaching:latest \
  $(aws sts get-caller-identity --query Account --output text).dkr.ecr.ap-northeast-1.amazonaws.com/gpu-teaching:latest
docker push \
  $(aws sts get-caller-identity --query Account --output text).dkr.ecr.ap-northeast-1.amazonaws.com/gpu-teaching:latest
```

Copy the full image URI and update `ECR_IMAGE_URI` in your `.env`.

### 4. Create AWS Batch resources

Run these in order. Replace `<ECR_IMAGE_URI>` with the value from your `.env`.

**Compute Environment** (uses g4dn.xlarge Spot — cheapest GPU instance):

```bash
aws batch create-compute-environment \
  --compute-environment-name gpu-teaching-ce \
  --type MANAGED \
  --state ENABLED \
  --compute-resources '{
    "type": "SPOT",
    "allocationStrategy": "SPOT_CAPACITY_OPTIMIZED",
    "minvCpus": 0,
    "maxvCpus": 8,
    "instanceTypes": ["g4dn.xlarge"],
    "subnets": ["<your-subnet-id>"],
    "securityGroupIds": ["<your-sg-id>"],
    "instanceRole": "arn:aws:iam::<account>:instance-profile/ecsInstanceRole"
  }' \
  --region ap-northeast-1
```

> **Tip**: `subnets` and `securityGroupIds` — use the defaults from your VPC. Run `aws ec2 describe-subnets` to find them.

**Job Queue**:

```bash
aws batch create-job-queue \
  --job-queue-name gpu-teaching-queue \
  --state ENABLED \
  --priority 1 \
  --compute-environment-order '[{"order": 1, "computeEnvironment": "gpu-teaching-ce"}]' \
  --region ap-northeast-1
```

**Job Definition**:

```bash
aws batch register-job-definition \
  --job-definition-name gpu-teaching-job-def \
  --type container \
  --container-properties '{
    "image": "<ECR_IMAGE_URI>",
    "vcpus": 4,
    "memory": 14000,
    "resourceRequirements": [{"type": "GPU", "value": "1"}],
    "jobRoleArn": "arn:aws:iam::<account>:role/BatchJobRole"
  }' \
  --region ap-northeast-1
```

Update `BATCH_JOB_QUEUE` and `BATCH_JOB_DEFINITION` in your `.env`.

---

## 🛠️ Pre-flight & Teardown

Before provisioning Batch infrastructure, validate GPU capacity in your VPC
(checks instance-type availability, Spot pricing/placement, and a dry-run
launch for Spot and/or On-Demand):

```bash
python helpers/check_spot_availability.py \
  --vpc-id        vpc-xxxxxxxxxxxxxxxxx \
  --subnet-id     subnet-xxxxxxxxxxxxxxxxx \
  --security-group-id sg-xxxxxxxxxxxxxxxxx
```

This prints a clear ✅ / ⚠️ / ❌ verdict for the requested capacity type(s)
(`--capacity-type spot|on-demand|both`, default `both`).

To tear down all course infrastructure when you're done:

```bash
# Preview what will be deleted:
python helpers/teardown.py --dry-run

# Delete Batch resources (job queues, compute envs, job definitions):
python helpers/teardown.py

# Delete everything including ECR and S3:
python helpers/teardown.py --delete-ecr --delete-s3
```

See [`helpers/README.md`](helpers/README.md) for full documentation.

---

## 📁 Repo Structure

```
gpu-teaching/
├── .env.example          ← template; copy to .env
├── README.md             ← you are here
├── Dockerfile            ← one shared image for all lessons
├── helpers/
│   ├── README.md
│   ├── check_spot_availability.py  ← pre-flight spot/on-demand check
│   └── teardown.py                 ← clean up all AWS resources
└── lessons/              ← 6 lessons; each = numbered demo steps in subfolders
    ├── 00-docker-build/
    ├── 01-why-gpu/
    ├── 02-first-batch-job/
    ├── 03-images-to-captions/
    ├── 04-full-pipeline/
    └── 05-scale-and-cost/
```

---

## 💡 How lessons work

Every lesson is a sequence of small, numbered steps — **one folder per demo**:

```
lessons/03-images-to-captions/
├── README.md                          ← theory + the step index
├── 01-upload-images/main.py           ← one tiny script per step
├── 02-caption-one-image/{job,main}.py
├── 03-caption-whole-batch/generate_captions.py
└── ...
```

Each step folder contains a `main.py` (or the container job script) plus a
mini-README with the exact command and expected output. The habit is always
the same: **cd into a step, run `python main.py`.**

Scripts that run on AWS Batch keep descriptive names (`job.py`,
`generate_captions.py`, `verify_captions.py`) — Batch references them by path
in the job's `command` override.

Every Batch job follows the same pattern:

```
download input from S3 → process on the GPU → upload results to S3
```

---

## 💰 Estimated Cost

A single `g4dn.xlarge` Spot instance costs roughly **$0.16–0.24/hr** in Tokyo.
Each lesson job runs for 2–5 minutes → **< $0.02 per lesson run**.
