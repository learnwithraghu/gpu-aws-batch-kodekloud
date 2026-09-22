"""
Lesson 03 · Step 04 — submit-and-wait
Submit the whole-batch captioning job (03-caption-whole-batch) and poll
until it finishes.

Run:  python main.py [--batch-stem sample]
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

batch = boto3.client("batch", region_name=REGION)

parser = argparse.ArgumentParser(description="Submit the batch captioning job.")
parser.add_argument("--batch-stem", default="sample")
parser.add_argument("--batch-size", type=int, default=8, help="Images captioned per GPU batch")
args = parser.parse_args()

response = batch.submit_job(
    jobName=f"lesson-03-generate-captions-{args.batch_stem}",
    jobQueue=JOB_QUEUE,
    jobDefinition=JOB_DEFINITION,
    containerOverrides={
        "command": ["python",
                    "/app/lessons/03-images-to-captions/03-caption-whole-batch/generate_captions.py"],
        "environment": [
            {"name": "S3_BUCKET",    "value": S3_BUCKET},
            {"name": "IMAGE_PREFIX", "value": f"images/{args.batch_stem}"},
            {"name": "BATCH_SIZE",   "value": str(args.batch_size)},
        ],
    },
)

job_id = response["jobId"]
print(f"Submitted job : {job_id}")

print("Polling every 10 s ...")
terminal = {"SUCCEEDED", "FAILED"}
while True:
    status = batch.describe_jobs(jobs=[job_id])["jobs"][0]["status"]
    print(f"  Status: {status}")
    if status in terminal:
        break
    time.sleep(10)

print(f"\n{'✅' if status == 'SUCCEEDED' else '❌'}  Job {status}")
print(f"Captions: s3://{S3_BUCKET}/captions/{args.batch_stem}/captions.csv")
