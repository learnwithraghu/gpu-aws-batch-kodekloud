# Step 03 — Build, tag, push, verify

The full image pipeline. **First run** is often **15–25 minutes** end-to-end:

| Phase | Typical time | Why |
|-------|----------------|-----|
| Pull CUDA base | ~8–12 min | `pytorch/pytorch:…-runtime` is ~3 GB (once; cached locally) |
| `pip install` | ~2–5 min | transformers + deps |
| Push to ECR | ~5–15 min | uploads the full image |

Re-runs after a lesson-only change reuse cached layers and finish in **under a
minute** (plus push if you changed the image). Use `helpers/push_ecr_image.sh
--pull-base` only when you intentionally refresh the PyTorch base tag.

If Docker dies mid-build/push (`Bad response from Docker engine`), raise
**Docker Desktop → Settings → Resources → Memory** to **8 GB**, quit Docker
fully, reopen, and retry. Step 02 (ECR repo) is handled by the helper below.

**Run (recommended — idempotent helper does all of the below):**

```bash
bash helpers/push_ecr_image.sh
```

This ensures the ECR repository exists (creating it if missing), authenticates
Docker with ECR, builds the image, pushes `gpu-teaching:latest`, verifies it
landed, and writes `ECR_IMAGE_URI` into your `.env`. Re-run it any time you
change the Dockerfile or lesson code.

<details>
<summary>Manual steps (equivalent, for learning what the helper does)</summary>

```bash
# 1. Authenticate Docker with ECR (token valid 12 hours)
aws ecr get-login-password --region ap-northeast-1 \
  | docker login --username AWS --password-stdin \
    $(aws sts get-caller-identity --query Account --output text).dkr.ecr.ap-northeast-1.amazonaws.com

# 2. Build from the repo root
docker build -t gpu-teaching .

# 3. Tag and push
ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
REPO=${ACCOUNT}.dkr.ecr.ap-northeast-1.amazonaws.com/gpu-teaching
docker tag gpu-teaching:latest ${REPO}:latest
docker push ${REPO}:latest

# 4. Verify it landed
aws ecr describe-images --repository-name gpu-teaching \
  --image-ids imageTag=latest --region ap-northeast-1
```

</details>

**Expected:** the helper prints "created" (first run only), `Login Succeeded`,
a pushed image, and a verification line. `ECR_IMAGE_URI` in `.env` is updated
automatically.
