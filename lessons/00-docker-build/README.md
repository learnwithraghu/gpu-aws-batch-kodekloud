# Lesson 00 — Building and Pushing the GPU Docker Image

> **Concepts**: Docker layers · CUDA base images · ECR authentication · image tagging  
> **AWS needed**: Amazon ECR

---

## Why Docker for GPU Workloads?

When you run a job on a GPU instance, you can't just send a Python script — you need to send an entire environment:

- The right CUDA version (must match the GPU driver on the instance)
- Python, PyTorch, Transformers (BLIP + CLIP), Pillow, boto3, …
- Your lesson code

Docker packages all of that into a single image. The same image runs on your laptop (for testing), on any g4dn.xlarge in AWS, and on any other GPU instance anywhere.

| Without Docker | With Docker |
|----------------|-------------|
| "Works on my machine" | Same environment everywhere |
| Manual CUDA driver matching | Pinned base image handles it |
| Dependency conflicts between lessons | Clean, isolated layer |
| AWS Batch can't run raw `.py` files | Batch pulls and runs your image |

---

## Anatomy of the Dockerfile

The entire course uses **one shared image** (`Dockerfile` at the repo root):

```dockerfile
# Base: official PyTorch image — CUDA 11.8 matches the g4dn.xlarge (NVIDIA T4) GPU driver
FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

# All Python dependencies for every lesson, installed in a single layer
# transformers provides both BLIP (image captioning) and CLIP (text embeddings)
RUN pip install --no-cache-dir \
    transformers>=4.42      \
    Pillow                  \
    boto3                   \
    python-dotenv           \
    numpy

# Copy all lesson scripts into the image
# AWS Batch overrides the "command" field at submit time
# to run the specific lesson script (e.g. "python lessons/02-.../job.py")
WORKDIR /app
COPY lessons/ /app/lessons/
```

Three things to notice:

1. **`pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime`** — this is the base. It bundles Python + PyTorch + CUDA 11.8 + cuDNN 8. The g4dn.xlarge runs the NVIDIA driver that supports CUDA 11.x, so this version is intentional.

2. **One `RUN pip install` layer** — Docker caches each instruction as a layer. Keeping all installs in one `RUN` means a single cache miss rebuilds them all at once (avoiding a stale partial cache).

3. **`COPY lessons/`** — every lesson script is baked into the image. Batch picks the right script at runtime via the `command` override in `submit_job.py`.

---

## What is ECR?

Amazon ECR (Elastic Container Registry) is AWS's private Docker registry.

| | Docker Hub | Amazon ECR |
|--|-----------|------------|
| Auth | Docker login | AWS IAM |
| Cost | Free tier limits, then $5/mo | $0.10/GB/month stored |
| Access | Public by default | Private, IAM-controlled |
| Batch integration | Needs credentials | Native — Batch pulls without extra config |

We use ECR because AWS Batch can pull from it directly using the IAM role attached to the Batch compute environment. No credentials to manage.

---

## How to Run

Open `notebook.ipynb` and run all cells top-to-bottom. It will walk you through each step interactively.

If you prefer the command line, here is the full sequence:

### Step 1 — Create the ECR repository (once)

```bash
aws ecr create-repository \
  --repository-name gpu-teaching \
  --region ap-northeast-1
```

### Step 2 — Authenticate Docker with ECR

```bash
aws ecr get-login-password --region ap-northeast-1 \
  | docker login --username AWS --password-stdin \
    $(aws sts get-caller-identity --query Account --output text).dkr.ecr.ap-northeast-1.amazonaws.com
```

You'll see `Login Succeeded`.

### Step 3 — Build the image

```bash
docker build -t gpu-teaching .
```

This takes 3–8 minutes the first time (downloading the ~3 GB base image and installing packages). Subsequent builds are fast because Docker caches each layer.

### Step 4 — Tag and push

```bash
ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
REGION=ap-northeast-1
REPO=${ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com/gpu-teaching

docker tag gpu-teaching:latest ${REPO}:latest
docker push ${REPO}:latest
```

### Step 5 — Update `.env`

Copy the full image URI and paste it into your `.env`:

```
ECR_IMAGE_URI=<account>.dkr.ecr.ap-northeast-1.amazonaws.com/gpu-teaching:latest
```

---

## Local Testing (optional)

You can run the image locally on CPU to verify it starts correctly:

```bash
docker run --rm gpu-teaching python -c "import torch, transformers, PIL, boto3; print('All imports OK')"
```

To test with a local GPU (if you have one):

```bash
docker run --rm --gpus all gpu-teaching python -c "import torch; print(torch.cuda.get_device_name(0))"
```

---

## Key Takeaway

> The Docker image is the **unit of deployment** for all GPU work in this course.  
> Build it once, push it to ECR, and every lesson uses it — you never touch the image again unless you add a new Python dependency.
