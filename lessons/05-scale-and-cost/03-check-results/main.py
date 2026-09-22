"""
Lesson 05 · Step 03 — check-results
List every caption folder in S3 and count the caption rows in each.

Run:  python main.py
"""
import csv
import io
import os

import boto3
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../../.env"))

S3_BUCKET = os.environ["S3_BUCKET"]
REGION    = os.environ.get("AWS_DEFAULT_REGION", "ap-northeast-1")

s3 = boto3.client("s3", region_name=REGION)

# 1. Find every captions/<stem>/captions.csv in the bucket
stems = set()
paginator = s3.get_paginator("list_objects_v2")
for page in paginator.paginate(Bucket=S3_BUCKET, Prefix="captions/"):
    for obj in page.get("Contents", []):
        parts = obj["Key"].split("/")
        if len(parts) == 3 and parts[2] == "captions.csv":
            stems.add(parts[1])

# 2. Count the rows in each
if not stems:
    print(f"No caption files yet in s3://{S3_BUCKET}/captions/")
else:
    print(f"Caption files in s3://{S3_BUCKET}/captions/:\n")
    total = 0
    for stem in sorted(stems):
        key = f"captions/{stem}/captions.csv"
        body = s3.get_object(Bucket=S3_BUCKET, Key=key)["Body"].read()
        rows = list(csv.DictReader(io.StringIO(body.decode())))
        total += len(rows)
        print(f"  {stem:>15} : {len(rows):>4} captions")
    print(f"\n  {'TOTAL':>15} : {total:>4} captions")
