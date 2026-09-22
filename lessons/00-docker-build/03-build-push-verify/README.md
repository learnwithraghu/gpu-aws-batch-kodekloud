# Step 03 — Build, tag, push, verify

The full image pipeline. Build takes 3–8 minutes the first time (~3 GB base
image); later builds are fast because Docker caches each layer.

**Run:**

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

**Expected:** `Login Succeeded`, a pushed image, and JSON showing tag
`latest`. Then set `ECR_IMAGE_URI=${REPO}:latest` in your `.env`.
