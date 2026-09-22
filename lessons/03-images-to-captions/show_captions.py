"""
Lesson 03 — show_captions.py
Runs LOCALLY. Downloads captions.csv for an image batch from S3 and prints
the image → caption table.

Usage:
    python show_captions.py [--batch-stem sample]
"""
import argparse
import csv
import io
import os

import boto3
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

S3_BUCKET = os.environ["S3_BUCKET"]
REGION    = os.environ.get("AWS_DEFAULT_REGION", "ap-northeast-1")

s3 = boto3.client("s3", region_name=REGION)


def load_captions(batch_stem: str) -> list[dict]:
    """Download captions/<batch_stem>/captions.csv and return the rows."""
    key = f"captions/{batch_stem}/captions.csv"
    obj = s3.get_object(Bucket=S3_BUCKET, Key=key)
    reader = csv.DictReader(io.StringIO(obj["Body"].read().decode()))
    return list(reader)


def main():
    parser = argparse.ArgumentParser(description="Print the caption file for an image batch.")
    parser.add_argument("--batch-stem", default="sample",
                        help="Image batch name (folder under captions/ in S3)")
    args = parser.parse_args()

    rows = load_captions(args.batch_stem)
    print(f"{len(rows)} captions in s3://{S3_BUCKET}/captions/{args.batch_stem}/captions.csv\n")

    for i, row in enumerate(rows, start=1):
        print(f"{i:3d}. {row['caption']}")
        print(f"      {row['image_s3_uri']}")


if __name__ == "__main__":
    main()
