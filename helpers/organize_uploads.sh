#!/usr/bin/env bash
# Sort root-level image uploads in the images bucket into the prefix layout
# the Batch jobs expect (images/<stem>/).
#
# The lesson jobs always caption images from an s3://<images-bucket>/images/<stem>/
# prefix. This helper finds image objects sitting at the bucket root (no "/")
# and moves them into images/<stem>/ (default stem: sample).
#
# Usage:
#   helpers/organize_uploads.sh [--stem sample] [--bucket <name>] [--dry-run]
#
#   --stem <stem>     Target batch folder (default: sample)
#   --bucket <name>   Override the images bucket (default: S3_IMAGES_BUCKET
#                     from .env, falling back to S3_BUCKET)
#   --dry-run         Show what would move without moving anything
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
ENV_FILE="$REPO_ROOT/.env"

STEM="sample"
BUCKET=""
DRY_RUN=false
while [ $# -gt 0 ]; do
  case "$1" in
    --stem)  STEM="$2"; shift 2 ;;
    --bucket) BUCKET="$2"; shift 2 ;;
    --dry-run) DRY_RUN=true; shift ;;
    -h|--help)
      echo "Usage: helpers/organize_uploads.sh [--stem sample] [--bucket <name>] [--dry-run]"
      echo ""
      echo "Moves root-level images in the S3 images bucket into images/<stem>/"
      exit 0 ;;
    *)
      echo "Unknown option: $1" >&2
      echo "Usage: helpers/organize_uploads.sh [--stem sample] [--bucket <name>] [--dry-run]" >&2
      exit 2 ;;
  esac
done

# Region so the AWS CLI talks to the right place
REGION="${REGION:-$(grep -E '^AWS_DEFAULT_REGION=' "$ENV_FILE" 2>/dev/null | cut -d= -f2)}"
export AWS_DEFAULT_REGION="${REGION:-$(aws configure get region)}"
BUCKET="${BUCKET:-$(grep -E '^S3_IMAGES_BUCKET=' "$ENV_FILE" 2>/dev/null | cut -d= -f2)}"
BUCKET="${BUCKET:-$(grep -E '^S3_BUCKET=' "$ENV_FILE" 2>/dev/null | cut -d= -f2)}"
if [ -z "$BUCKET" ]; then
  echo "Error: no images bucket found. Pass --bucket or run helpers/create_buckets.sh first." >&2
  exit 1
fi

DEST_PREFIX="images/${STEM}"
COUNT=0

echo "Bucket   : s3://$BUCKET"
echo "Moving to: $DEST_PREFIX/"
echo

while IFS= read -r key; do
  COUNT=$((COUNT + 1))
  filename="$(basename "$key")"
  if [ "$DRY_RUN" = "true" ]; then
    echo "[dry]  would move: $key → $DEST_PREFIX/$filename"
  else
    aws s3api copy-object \
      --bucket "$BUCKET" \
      --copy-source "$BUCKET/$key" \
      --key "$DEST_PREFIX/$filename"
    aws s3api delete-object --bucket "$BUCKET" --key "$key"
    echo "[ok]   moved: $key → $DEST_PREFIX/$filename"
  fi
done < <(
  aws s3api list-objects-v2 --bucket "$BUCKET" \
    --query "Contents[?!contains(Key, '/')].[Key]" --output text
)

if [ "$COUNT" -eq 0 ]; then
  echo "No root-level images found — nothing to move."
  exit 0
fi

echo
if [ "$DRY_RUN" = "true" ]; then
  echo "$COUNT root-level image(s) would be moved. Re-run without --dry-run to apply."
else
  echo "Done. Moved $COUNT image(s) to s3://$BUCKET/$DEST_PREFIX/"
fi
