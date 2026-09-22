#!/usr/bin/env bash
# Create the course S3 buckets (idempotent — skip if they already exist):
#   - images bucket       : raw images, uploaded manually by the tutor
#   - captions-csv bucket : CSV files mapping each image to its caption
#
# Bucket names are suffixed with the AWS account ID so they are unique and
# never collide with other tutors' buckets. Resolved names are written back
# to .env as S3_IMAGES_BUCKET and S3_CSV_BUCKET (if not already present).
#
# Usage:
#   helpers/create_buckets.sh [--region <region>]
#
#   --region <region>  Override the region (default: AWS_DEFAULT_REGION from
#                      .env, or the AWS CLI default)
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
ENV_FILE="$REPO_ROOT/.env"

REGION=""
while [ $# -gt 0 ]; do
  case "$1" in
    --region)
      [ $# -ge 2 ] || { echo "Error: --region requires a value" >&2; exit 2; }
      REGION="$2"; shift 2 ;;
    -h|--help)
      echo "Usage: helpers/create_buckets.sh [--region <region>]"
      echo ""
      echo "Creates the course S3 buckets (images + captions CSV) if missing."
      echo "  --region <region>  Override the AWS region"
      exit 0 ;;
    *)
      echo "Unknown option: $1" >&2
      echo "Usage: helpers/create_buckets.sh [--region <region>]" >&2
      exit 2 ;;
  esac
done

REGION="${REGION:-$(grep -E '^AWS_DEFAULT_REGION=' "$ENV_FILE" 2>/dev/null | cut -d= -f2)}"
REGION="${REGION:-$(aws configure get region)}"
if [ -z "$REGION" ]; then
  echo "Error: no region found. Pass --region or set AWS_DEFAULT_REGION in .env." >&2
  exit 1
fi

ACCOUNT_ID="$(aws sts get-caller-identity --query Account --output text)" || {
  echo "Error: failed to get AWS account ID — check your AWS CLI credentials." >&2
  exit 1
}

IMAGES_BUCKET="gpu-teaching-images-${ACCOUNT_ID}"
CSV_BUCKET="gpu-teaching-captions-csv-${ACCOUNT_ID}"

create_bucket() {
  local bucket="$1"
  if aws s3api head-bucket --bucket "$bucket" 2>/dev/null; then
    echo "[skip] s3://$bucket already exists"
    return 0
  fi
  local -a args=(--bucket "$bucket" --region "$REGION")
  # us-east-1 rejects a LocationConstraint; every other region requires it.
  [ "$REGION" != "us-east-1" ] && args+=(--create-bucket-configuration "LocationConstraint=$REGION")
  if aws s3api create-bucket "${args[@]}"; then
    echo "[ok]   created s3://$bucket"
  else
    echo "[fail] could not create s3://$bucket" >&2
    return 1
  fi
}

FAILED=0
echo "Region: $REGION"
echo "Creating S3 buckets…"
create_bucket "$IMAGES_BUCKET" || FAILED=1
create_bucket "$CSV_BUCKET"    || FAILED=1
if [ "$FAILED" -ne 0 ]; then
  echo "Bucket creation failed — fix the errors above and re-run." >&2
  exit 1
fi

# Persist bucket names in .env so lessons and teardown.py pick them up.
if [ ! -f "$ENV_FILE" ]; then
  cp "$REPO_ROOT/.env.example" "$ENV_FILE" 2>/dev/null || touch "$ENV_FILE"
fi

set_env_var() {
  local key="$1" value="$2"
  if grep -qE "^${key}=" "$ENV_FILE"; then
    sed -i "s|^${key}=.*|${key}=${value}|" "$ENV_FILE"
  else
    printf '%s=%s\n' "$key" "$value" >> "$ENV_FILE"
  fi
}

# S3_BUCKET is kept for lessons that use the legacy single-bucket variable.
set_env_var "AWS_DEFAULT_REGION" "$REGION"
set_env_var "S3_IMAGES_BUCKET"   "$IMAGES_BUCKET"
set_env_var "S3_CSV_BUCKET"      "$CSV_BUCKET"
set_env_var "S3_BUCKET"          "$IMAGES_BUCKET"

echo
echo "Done. Buckets written to .env:"
echo "  S3_IMAGES_BUCKET = $IMAGES_BUCKET"
echo "  S3_CSV_BUCKET    = $CSV_BUCKET"
