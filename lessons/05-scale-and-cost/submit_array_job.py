"""
Lesson 05 — submit_array_job.py
Runs LOCALLY. Captions multiple image batches in parallel using a Batch array job.

Each array element reads its index from AWS_BATCH_JOB_ARRAY_INDEX, looks up
the corresponding image prefix in a JSON list stored in S3, and runs
generate_captions.py on that batch.

Usage:
    # First upload your image batches to S3 (or use lesson 03's submit_job.py):
    aws s3 cp images/ s3://<bucket>/images/ --recursive

    # Then submit an array job (one element per image batch/prefix):
    python submit_array_job.py --image-prefixes images/batch1 images/batch2 images/batch3
"""
import argparse
import json
import os
import time

import boto3
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

S3_BUCKET      = os.environ["S3_BUCKET"]
JOB_QUEUE      = os.environ["BATCH_JOB_QUEUE"]
JOB_DEFINITION = os.environ["BATCH_JOB_DEFINITION"]
REGION         = os.environ.get("AWS_DEFAULT_REGION", "ap-northeast-1")

s3    = boto3.client("s3",    region_name=REGION)
batch = boto3.client("batch", region_name=REGION)

# The list of image prefixes is stored in S3 so every array element can read it
IMAGE_PREFIX_LIST_KEY = "config/array_image_prefixes.json"


def upload_image_prefix_list(image_prefixes: list[str]):
    """Save the list of image S3 prefixes to S3 so each array element can read it."""
    body = json.dumps(image_prefixes).encode()
    s3.put_object(Bucket=S3_BUCKET, Key=IMAGE_PREFIX_LIST_KEY, Body=body)
    print(f"Saved {len(image_prefixes)} image prefixes to s3://{S3_BUCKET}/{IMAGE_PREFIX_LIST_KEY}")


def submit_array(n: int) -> str:
    """Submit one array job with n elements. Returns the array job ID."""
    response = batch.submit_job(
        jobName       = "lesson-05-array-caption",
        jobQueue      = JOB_QUEUE,
        jobDefinition = JOB_DEFINITION,
        arrayProperties= {"size": n},      # ← this is what makes it an array job
        containerOverrides={
            # Each element runs this command:
            # 1. Read the image prefix list from S3
            # 2. Pick the prefix at index = AWS_BATCH_JOB_ARRAY_INDEX
            # 3. Run generate_captions.py on that image batch
            "command": [
                "bash", "-c",
                (
                    "IMAGE_PREFIX=$(python3 -c \""
                    "import boto3, json, os; "
                    "s3=boto3.client('s3'); "
                    "prefixes=json.loads(s3.get_object(Bucket=os.environ['S3_BUCKET'], "
                    "Key=os.environ['IMAGE_PREFIX_LIST_KEY'])['Body'].read()); "
                    "print(prefixes[int(os.environ['AWS_BATCH_JOB_ARRAY_INDEX'])])\") && "
                    "IMAGE_PREFIX=$IMAGE_PREFIX python /app/lessons/03-images-to-captions/generate_captions.py"
                )
            ],
            "environment": [
                {"name": "S3_BUCKET",           "value": S3_BUCKET},
                {"name": "IMAGE_PREFIX_LIST_KEY", "value": IMAGE_PREFIX_LIST_KEY},
            ],
        },
    )
    job_id = response["jobId"]
    print(f"Submitted array job: {job_id}  (size={n})")
    return job_id


def wait(job_id: str) -> str:
    """Poll until all array elements finish."""
    terminal = {"SUCCEEDED", "FAILED"}
    print("Polling every 20 s ...")
    while True:
        resp  = batch.describe_jobs(jobs=[job_id])
        job   = resp["jobs"][0]
        state = job["status"]
        arr   = job.get("arrayProperties", {}).get("statusSummary", {})
        print(f"  Overall: {state}  |  {arr}")
        if state in terminal:
            return state
        time.sleep(20)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--image-prefixes", nargs="+",
        default=["images/sample"],
        help="S3 prefixes of image batches to caption (already uploaded to S3)",
    )
    args = parser.parse_args()

    upload_image_prefix_list(args.image_prefixes)

    final_state = wait(submit_array(len(args.image_prefixes)))
    print(f"\n{'✅' if final_state == 'SUCCEEDED' else '❌'}  Array job {final_state}")
    print(f"Caption files are under s3://{S3_BUCKET}/captions/<batch-name>/captions.csv")
