# Lesson 04 — Create the ECR repository and push

Batch pulls from Amazon ECR. This lesson creates the `gpu-teaching` repository, logs Docker in, and pushes the image you built in lesson 03.

Theory reading: [`theory.md`](theory.md).

From the repo root, with the AWS CLI configured for `ap-northeast-1`:

```bash
export AWS_DEFAULT_REGION=ap-northeast-1
export ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export REGISTRY="${ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com"
echo "$REGISTRY"
```

## Create the repository

Skip creation when the name already exists.

```bash
aws ecr describe-repositories --repository-names gpu-teaching --region "$AWS_DEFAULT_REGION"
```

If that fails with `RepositoryNotFoundException`:

```bash
aws ecr create-repository \
  --repository-name gpu-teaching \
  --image-scanning-configuration scanOnPush=true \
  --region "$AWS_DEFAULT_REGION"
```

The repository name is `gpu-teaching`. The image tag you will push is `latest`.

## Log Docker in to ECR

The password lasts 12 hours. Run this again before a later push if Docker says the login expired.

```bash
aws ecr get-login-password --region "$AWS_DEFAULT_REGION" \
  | docker login --username AWS --password-stdin "$REGISTRY"
```

## Tag and push

```bash
docker tag gpu-teaching:latest "${REGISTRY}/gpu-teaching:latest"
docker push "${REGISTRY}/gpu-teaching:latest"
```

The push is large the first time (about 3.8 GB). Later pushes send only the layers that changed.

## Check, and write `.env`

```bash
aws ecr describe-images \
  --repository-name gpu-teaching \
  --image-ids imageTag=latest \
  --region "$AWS_DEFAULT_REGION" \
  --query 'imageDetails[0].{pushed:imagePushedAt,size:imageSizeInBytes}'
```

Copy `.env.example` to `.env` if you do not have one yet, and set:

```bash
ECR_IMAGE_URI=${REGISTRY}/gpu-teaching:latest
```

Use your real registry in that line. The job definition in lesson 07 points at this URI. A new push of `:latest` is what the next job pulls. A job that already started keeps the image it pulled.
