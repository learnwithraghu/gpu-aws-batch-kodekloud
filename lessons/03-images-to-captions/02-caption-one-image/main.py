"""
Lesson 03 · Step 02 — caption-one-image (main.py)
Submit job.py to Batch so ONE sample image gets captioned on the GPU.

Run:  python main.py [--batch-stem sample] [--image <filename>]
"""
import argparse
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

parser = argparse.ArgumentParser(description="Caption one image on the GPU.")
parser.add_argument("--batch-stem", default="sample")
parser.add_argument("--image", default=None, help="Image filename; default = first uploaded image")
args = parser.parse_args()

# Pick the image key (first one under the prefix unless --image is given)
prefix = f"images/{args.batch_stem}/"
if args.image:
    image_key = f"{prefix}{args.image}"
else:
    page = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=prefix, MaxKeys=20)
    keys = [o["Key"] for o in page.get("Contents", [])
            if o["Key"].lower().endswith((".jpg", ".jpeg", ".png"))]
    if not keys:
        raise FileNotFoundError(
            f"No images under s3://{S3_BUCKET}/{prefix} — run 01-upload-images first"
        )
    image_key = keys[0]

response = batch.submit_job(
    jobName="lesson-03-caption-one",
    jobQueue=JOB_QUEUE,
    jobDefinition=JOB_DEFINITION,
    containerOverrides={
        "command": ["python", "/app/lessons/03-images-to-captions/02-caption-one-image/job.py"],
        "environment": [
            {"name": "S3_BUCKET", "value": S3_BUCKET},
            {"name": "IMAGE_KEY", "value": image_key},
        ],
    },
)

job_id = response["jobId"]
print(f"Submitted job : {job_id}")
print(f"Image         : s3://{S3_BUCKET}/{image_key}")

print("Polling every 10 s ...")
terminal = {"SUCCEEDED", "FAILED"}
while True:
    status = batch.describe_jobs(jobs=[job_id])["jobs"][0]["status"]
    print(f"  Status: {status}")
    if status in terminal:
        break
    time.sleep(10)

print(f"\n{'✅' if status == 'SUCCEEDED' else '❌'}  Job {status}")
print("Open the CloudWatch log stream to see: Device / Image / Caption")
