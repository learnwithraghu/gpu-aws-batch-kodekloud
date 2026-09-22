"""
Lesson 04 — verify_captions.py
Runs INSIDE the Docker container as Job 2 of the pipeline. Batch only starts
it after Job 1 (generate_captions.py) reaches SUCCEEDED.

Downloads the caption file produced by Job 1, checks that every image in the
image prefix has exactly one caption, prints a short report, and writes a
_VERIFIED marker to S3. Exits non-zero (fails the Batch job) on any mismatch.

Environment variables (passed by Batch at submit time):
    S3_BUCKET     — the S3 bucket name
    IMAGE_PREFIX  — S3 prefix holding the input images, e.g. "images/sample"
"""
import csv
import io
import os

import boto3

S3_BUCKET    = os.environ["S3_BUCKET"]
IMAGE_PREFIX = os.environ["IMAGE_PREFIX"]     # e.g. "images/sample"

s3 = boto3.client("s3")


def count_images() -> int:
    """Count the image objects under the image prefix."""
    count = 0
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=S3_BUCKET, Prefix=f"{IMAGE_PREFIX}/"):
        count += sum(
            1 for obj in page.get("Contents", [])
            if obj["Key"].lower().endswith((".jpg", ".jpeg", ".png"))
        )
    return count


def load_captions() -> list[dict]:
    """Load the caption file produced by Job 1."""
    stem = os.path.basename(IMAGE_PREFIX.rstrip("/"))
    key = f"captions/{stem}/captions.csv"
    obj = s3.get_object(Bucket=S3_BUCKET, Key=key)
    return list(csv.DictReader(io.StringIO(obj["Body"].read().decode())))


def main():
    n_images = count_images()
    captions = load_captions()

    print(f"Images in s3://{S3_BUCKET}/{IMAGE_PREFIX}/ : {n_images}")
    print(f"Captions in captions file              : {len(captions)}")

    if len(captions) != n_images:
        print("MISMATCH — every image must have exactly one caption.")
        raise SystemExit(1)

    print("\nFirst 5 captions:")
    for row in captions[:5]:
        print(f"  {row['image_s3_uri']}  →  {row['caption']}")

    stem = os.path.basename(IMAGE_PREFIX.rstrip("/"))
    marker_key = f"captions/{stem}/_VERIFIED"
    s3.put_object(Bucket=S3_BUCKET, Key=marker_key, Body=b"ok")
    print(f"\nVerification passed. Marker written to s3://{S3_BUCKET}/{marker_key}")


if __name__ == "__main__":
    main()
