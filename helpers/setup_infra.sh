#!/usr/bin/env bash
# Tutor helper: spin the course infrastructure up and down quickly.
#
#   helpers/setup_infra.sh up    Provision S3 buckets (images + captions CSV)
#   helpers/setup_infra.sh down  Tear everything down (Batch, ECR, S3, ...)
#
# "up" is idempotent: buckets that already exist are left alone, so it is safe
# to run repeatedly. "down" delegates to helpers/teardown.py, which confirms
# before deleting anything.
#
# Usage:
#   helpers/setup_infra.sh up|down [--region <region>] [--delete-ecr]
#                                  [--delete-s3] [--dry-run]
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

usage() {
  echo "Usage: helpers/setup_infra.sh up|down [--region <region>] [--delete-ecr] [--delete-s3]"
  echo "                                   [--dry-run]"
  echo ""
  echo "  up        Create the S3 buckets (images + captions CSV); skips ones that exist"
  echo "  down      Tear down course resources via helpers/teardown.py"
  echo ""
  echo "  --region <region>  Override the AWS region"
  echo "  --delete-ecr       (down) also delete the ECR repository and its images"
  echo "  --delete-s3        (down) also empty and delete the S3 buckets"
  echo "  --dry-run          (down) show what would be deleted without deleting"
}

COMMAND=""
REGION=""
EXTRA_ARGS=()
while [ $# -gt 0 ]; do
  case "$1" in
    up|down)   COMMAND="$1"; shift ;;
    --region)
      [ $# -ge 2 ] || { echo "Error: --region requires a value" >&2; usage >&2; exit 2; }
      REGION="$2"; EXTRA_ARGS+=(--region "$2"); shift 2 ;;
    --delete-ecr)  EXTRA_ARGS+=(--delete-ecr);  shift ;;
    --delete-s3)   EXTRA_ARGS+=(--delete-s3);   shift ;;
    --dry-run)     EXTRA_ARGS+=(--dry-run);     shift ;;
    -h|--help)    usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

if [ -z "$COMMAND" ]; then
  usage >&2
  exit 2
fi

case "$COMMAND" in
  up)
    echo "── Spinning up course infrastructure ──"
    if [ -n "$REGION" ]; then
      bash "$SCRIPT_DIR/create_buckets.sh" --region "$REGION"
    else
      bash "$SCRIPT_DIR/create_buckets.sh"
    fi
    ;;
  down)
    echo "── Tearing down course infrastructure ──"
    UV=(uv run --with boto3 --with python-dotenv python)
    # teardown.py picks up S3_BUCKET / S3_IMAGES_BUCKET / S3_CSV_BUCKET from
    # the repo's .env on its own — nothing to export here.
    "${UV[@]}" "$SCRIPT_DIR/teardown.py" "${EXTRA_ARGS[@]}"
    ;;
esac
