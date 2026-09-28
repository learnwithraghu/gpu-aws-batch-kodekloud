#!/usr/bin/env bash
# Build the course GPU image and push it to Amazon ECR (idempotent).
#
#   1. Ensure the ECR repository exists (created if missing)
#   2. Authenticate Docker with ECR
#   3. Build the image from the repo-root Dockerfile
#   4. Tag and push :latest
#   5. Write ECR_IMAGE_URI=<repo>:latest into .env (if the container was
#      built before, this re-pushes the updated image — required after any
#      change to the Dockerfile or lessons/02-the-container-program/*.py)
#
# Usage:
#   helpers/push_ecr_image.sh [--region <region>] [--repo <name>] [--tag <tag>]
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
ENV_FILE="$REPO_ROOT/.env"
DEFAULT_REGION="ap-northeast-1"

REGION=""
REPO_NAME="gpu-teaching"
TAG="latest"
PULL_BASE=0
while [ $# -gt 0 ]; do
  case "$1" in
    --pull-base) PULL_BASE=1; shift ;;
    --repo) REPO_NAME="$2"; shift 2 ;;
    --tag)  TAG="$2"; shift 2 ;;
    --region)
      [ $# -ge 2 ] || { echo "Error: --region requires a value" >&2; exit 2; }
      REGION="$2"; shift 2 ;;
    -h|--help)
      echo "Usage: helpers/push_ecr_image.sh [--pull-base] [--region <region>] [--repo <name>] [--tag <tag>]"
      echo ""
      echo "Ensures the ECR repository exists, then builds and pushes the course"
      echo "GPU image (--tag, default latest) and updates ECR_IMAGE_URI in .env."
      exit 0 ;;
    *)
      echo "Unknown option: $1" >&2
      echo "Usage: helpers/push_ecr_image.sh [--pull-base] [--region <region>] [--repo <name>] [--tag <tag>]" >&2
      exit 2 ;;
  esac
done

REGION="${REGION:-$(grep -E '^AWS_DEFAULT_REGION=' "$ENV_FILE" 2>/dev/null | cut -d= -f2)}"
REGION="${REGION:-$(aws configure get region)}"
REGION="${REGION:-$DEFAULT_REGION}"
export AWS_DEFAULT_REGION="$REGION"

ACCOUNT_ID="$(aws sts get-caller-identity --query Account --output text)" || {
  echo "Error: failed to get AWS account ID — check your AWS CLI credentials." >&2
  exit 1
}
REGISTRY="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com"
ECR_IMAGE_URI="${REGISTRY}/${REPO_NAME}:${TAG}"

set_env_var() {
  local key="$1" value="$2"
  if [ -f "$ENV_FILE" ] && grep -qE "^${key}=" "$ENV_FILE"; then
    if sed --version 2>/dev/null | grep -q GNU; then
      sed -i "s|^${key}=.*|${key}=${value}|" "$ENV_FILE"
    else
      sed -i '' "s|^${key}=.*|${key}=${value}|" "$ENV_FILE"
    fi
  else
    printf '%s=%s\n' "$key" "$value" >> "$ENV_FILE"
  fi
}

set -e

if ! python3 -c "
import subprocess, sys
try:
    subprocess.run(['docker', 'info'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15, check=True)
except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
    sys.exit(1)
" 2>/dev/null; then
  echo "Error: Docker is not running or the engine is unhealthy." >&2
  echo "  Start Docker Desktop, wait until it is ready, then re-run this script." >&2
  echo "  If you see 'Bad response from Docker engine', raise Docker memory to 8 GB," >&2
  echo "  fully quit Docker, reopen, and try again (see PLAN.md step 2)." >&2
  exit 1
fi

# 1. Ensure the ECR repository exists
echo "[1/4] ECR repository    : $REPO_NAME"
if aws ecr describe-repositories --repository-names "$REPO_NAME" --region "$REGION" >/dev/null 2>&1; then
  echo "        already exists — skipping creation"
else
  aws ecr create-repository --repository-name "$REPO_NAME" \
    --image-scanning-configuration scanOnPush=true --region "$REGION" >/dev/null
  echo "        created"
fi

# 2. Authenticate Docker with ECR
echo "[2/4] Docker ECR login"
aws ecr get-login-password --region "$REGION" \
  | docker login --username AWS --password-stdin "$REGISTRY" >/dev/null

# 3. Build from the repo root (--pull-base re-downloads the ~3 GB CUDA base; default uses cache)
echo "[3/4] Building image    : gpu-teaching:${TAG}"
if [ "$PULL_BASE" -eq 1 ]; then
  docker build --platform linux/amd64 --pull -t "${REPO_NAME}:${TAG}" "$REPO_ROOT"
else
  docker build --platform linux/amd64 -t "${REPO_NAME}:${TAG}" "$REPO_ROOT"
fi

# 4. Tag and push
echo "[4/4] Pushing           : $ECR_IMAGE_URI"
docker tag "${REPO_NAME}:${TAG}" "$ECR_IMAGE_URI"
docker push "$ECR_IMAGE_URI"

set +e

# 5. Verify it landed
if aws ecr describe-images --repository-name "$REPO_NAME" \
     --image-ids imageTag="$TAG" --region "$REGION" >/dev/null 2>&1; then
  echo "Verified: $ECR_IMAGE_URI is in ECR"
else
  echo "Warning: could not verify the pushed image" >&2
fi

# 6. Record the image URI for the lesson submitters
set_env_var "ECR_IMAGE_URI" "$ECR_IMAGE_URI"
echo
echo "Done. Wrote ECR_IMAGE_URI to .env:"
echo "  $ECR_IMAGE_URI"
