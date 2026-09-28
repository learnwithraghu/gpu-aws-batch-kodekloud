"""Find the photos in S3, download one, and save the catalog CSV.

No GPU in this file. describe_items.py calls these three functions.
"""
import csv
import io
import os

import boto3
from PIL import Image

# Batch fills these in when the job is submitted. They are not hard-coded.
BUCKET = os.environ["S3_BUCKET"]
CSV_BUCKET = os.environ.get("S3_CSV_BUCKET", BUCKET)
PREFIX = os.environ["IMAGE_PREFIX"].strip("/")  # example: images/sample

s3 = boto3.client("s3")


def list_photo_keys():
    """Return the .jpg, .jpeg, and .png keys in the folder, in sorted order."""
    # One list call is enough for a vendor folder (S3 returns up to 1000 keys).
    response = s3.list_objects_v2(Bucket=BUCKET, Prefix=PREFIX + "/")

    keys = []
    for obj in response.get("Contents", []):
        key = obj["Key"]
        if key.lower().endswith((".jpg", ".jpeg", ".png")):
            keys.append(key)

    keys.sort()
    return keys


def download_photo(key):
    """Download one object and open it as an RGB picture."""
    body = s3.get_object(Bucket=BUCKET, Key=key)["Body"].read()
    return Image.open(io.BytesIO(body)).convert("RGB")


def save_csv(rows):
    """Write one CSV. rows is a list of (image_s3_uri, item_description)."""
    # images/sample -> sample, so the file lands at descriptions/sample/descriptions.csv
    folder = PREFIX.split("/")[-1]
    out_key = f"descriptions/{folder}/descriptions.csv"

    # csv.writer quotes a description that contains a comma.
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["image_s3_uri", "item_description"])
    writer.writerows(rows)

    s3.put_object(Bucket=CSV_BUCKET, Key=out_key, Body=buffer.getvalue().encode())
    print(f"Wrote {len(rows)} descriptions to s3://{CSV_BUCKET}/{out_key}")
