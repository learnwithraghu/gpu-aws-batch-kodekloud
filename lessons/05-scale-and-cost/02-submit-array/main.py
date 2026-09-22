"""
Lesson 05 · Step 02 — submit-array
Submit ONE array job that captions N image batches in parallel. Each element
reads its index from AWS_BATCH_JOB_ARRAY_INDEX, picks its image prefix from
a list stored in S3, and runs generate_captions.py on that batch.

Run:  python main.py --image-prefixes images/batch01 images/batch02 images/batch03
"""
import argparse
import json
import os
import time

import boto3
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../../.env"))

S3_BUCKET      = os.environ["S3_BUCKET"]
JOB_QUEUE      = os.environ["BATCH_JOB_QUEUE"]
JOB_DEFINITION = os.environ["BATCH_JOB_DEFINITION"]
REGION         = os.environ.get("AWS_DEFAULT_REGION", "ap-northeast-1")

s3    = boto3.client("s3",    region_name=REGION)
batch = boto3.client("batch", region_name=REGION)

# The list of image prefixes is stored in S3 so every array element can read it
IMAGE_PREFIX_LIST_KEY = "config/array_image_prefixes.json"

parser = argparse.ArgumentParser(description="Caption N image batches in parallel.")
parser.add_argument(
    "--image-prefixes", nargs="+", default=["images/sample"],
    help="S3 prefixes of image batches to caption (already uploaded to S3)",
)
args = parser.parse_args()

# 1. Save the prefix list to S3 so every array element can read it
body = json.dumps(args.image_prefixes).encode()
s3.put_object(Bucket=S3_BUCKET, Key=IMAGE_PREFIX_LIST_KEY, Body=body)
print(f"Saved {len(args.image_prefixes)} image prefixes to s3://{S3_BUCKET}/{IMAGE_PREFIX_LIST_KEY}")

# 2. Submit the array job — arrayProperties is what makes it an array job
response = batch.submit_job(
    jobName        = "lesson-05-array-caption",
    jobQueue       = JOB_QUEUE,
    jobDefinition  = JOB_DEFINITION,
    arrayProperties= {"size": len(args.image_prefixes)},
    containerOverrides={
        "command": [
            "bash", "-c",
            (
                "IMAGE_PREFIX=$(python3 -c \""
                "import boto3, json, os; "
                "s3=boto3.client('s3'); "
                "prefixes=json.loads(s3.get_object(Bucket=os.environ['S3_BUCKET'], "
                "Key=os.environ['IMAGE_PREFIX_LIST_KEY'])['Body'].read()); "
                "print(prefixes[int(os.environ['AWS_BATCH_JOB_ARRAY_INDEX'])])\") && "
                "IMAGE_PREFIX=$IMAGE_PREFIX python /app/lessons/03-images-to-captions/03-caption-whole-batch/generate_captions.py"
            )
        ],
        "environment": [
            {"name": "S3_BUCKET",             "value": S3_BUCKET},
            {"name": "IMAGE_PREFIX_LIST_KEY", "value": IMAGE_PREFIX_LIST_KEY},
        ],
    },
)

job_id = response["jobId"]
print(f"Submitted array job: {job_id}  (size={len(args.image_prefixes)})")

# 3. Poll until every element finishes
terminal = {"SUCCEEDED", "FAILED"}
print("Polling every 20 s ...")
while True:
    job   = batch.describe_jobs(jobs=[job_id])["jobs"][0]
    state = job["status"]
    summary = job.get("arrayProperties", {}).get("statusSummary", {})
    print(f"  Overall: {state}  |  {summary}")
    if state in terminal:
        break
    time.sleep(20)

print(f"\n{'✅' if state == 'SUCCEEDED' else '❌'}  Array job {state}")
print("Caption files are under s3://<bucket>/captions/<batch-name>/captions.csv")
