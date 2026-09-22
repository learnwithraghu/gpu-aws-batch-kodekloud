"""
Lesson 03 · Step 01 — upload-images
Upload the sample images in assets/images/ to S3.

Run:  python main.py [--batch-stem sample]
"""
import argparse
import glob
import os

import boto3
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../../.env"))

S3_BUCKET = os.environ["S3_BUCKET"]
REGION    = os.environ.get("AWS_DEFAULT_REGION", "ap-northeast-1")

s3 = boto3.client("s3", region_name=REGION)

parser = argparse.ArgumentParser(description="Upload sample images to S3.")
parser.add_argument("--images-dir",
                    default=os.path.join(os.path.dirname(__file__), "..", "assets", "images"),
                    help="Local folder of images")
parser.add_argument("--batch-stem", default="sample", help="S3 prefix name: images/<stem>")
args = parser.parse_args()

image_paths = sorted(
    p for ext in ("*.jpg", "*.jpeg", "*.png")
    for p in glob.glob(os.path.join(args.images_dir, ext))
)
if not image_paths:
    raise FileNotFoundError(f"No .jpg/.jpeg/.png images found in {args.images_dir}")

prefix = f"images/{args.batch_stem}"
for path in image_paths:
    s3_key = f"{prefix}/{os.path.basename(path)}"
    print(f"Uploading {os.path.basename(path)} → s3://{S3_BUCKET}/{s3_key}")
    s3.upload_file(path, S3_BUCKET, s3_key)

print(f"\nUploaded {len(image_paths)} images to s3://{S3_BUCKET}/{prefix}/")
