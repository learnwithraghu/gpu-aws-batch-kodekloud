"""
Lesson 03 · Step 05 — show-captions
Download captions.csv for an image batch from S3 and print the table.

Run:  python main.py [--batch-stem sample]
"""
import argparse
import csv
import io
import os

import boto3
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../../.env"))

S3_BUCKET      = os.environ["S3_BUCKET"]
S3_CSV_BUCKET  = os.environ.get("S3_CSV_BUCKET", S3_BUCKET)   # captions CSV bucket
REGION         = os.environ.get("AWS_DEFAULT_REGION", "ap-northeast-1")

s3 = boto3.client("s3", region_name=REGION)

parser = argparse.ArgumentParser(description="Print the caption file for an image batch.")
parser.add_argument("--batch-stem", default="sample", help="Folder under captions/ in S3")
args = parser.parse_args()

key = f"captions/{args.batch_stem}/captions.csv"
obj = s3.get_object(Bucket=S3_CSV_BUCKET, Key=key)
rows = list(csv.DictReader(io.StringIO(obj["Body"].read().decode())))

print(f"{len(rows)} captions in s3://{S3_CSV_BUCKET}/{key}\n")
for i, row in enumerate(rows, start=1):
    print(f"{i:3d}. {row['caption']}")
    print(f"      {row['image_s3_uri']}")
