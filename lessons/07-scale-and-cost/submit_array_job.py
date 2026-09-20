"""
Lesson 07 — submit_array_job.py
Runs LOCALLY. Processes multiple image batches in parallel using a Batch array job.

Each array element reads its index from AWS_BATCH_JOB_ARRAY_INDEX, looks up
the corresponding image prefix in a JSON list stored in S3, and runs the full
caption → embed pipeline.

Usage:
    # First upload all image batches to S3:
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
S3_VECTOR_BUCKET = os.environ["S3_VECTOR_BUCKET"]
S3_VECTOR_INDEX = os.environ["S3_VECTOR_INDEX"]
JOB_QUEUE      = os.environ["BATCH_JOB_QUEUE"]
JOB_DEFINITION = os.environ["BATCH_JOB_DEFINITION"]
REGION         = os.environ.get("AWS_DEFAULT_REGION", "ap-northeast-1")

s3    = boto3.client("s3",    region_name=REGION)
batch = boto3.client("batch", region_name=REGION)

# The array worker script (embedded inline to keep this lesson self-contained)
ARRAY_WORKER_KEY = "config/array_image_prefixes.json"


def upload_image_prefix_list(image_prefixes: list[str]):
    """Save the list of image S3 prefixes to S3 so each array element can read it."""
    body = json.dumps(image_prefixes).encode()
    s3.put_object(Bucket=S3_BUCKET, Key=ARRAY_WORKER_KEY, Body=body)
    print(f"Saved {len(image_prefixes)} image prefixes to s3://{S3_BUCKET}/{ARRAY_WORKER_KEY}")


def submit_array(n: int) -> str:
    """Submit one array job with n elements. Returns the array job ID."""
    response = batch.submit_job(
        jobName       = "lesson-07-array-pipeline",
        jobQueue      = JOB_QUEUE,
        jobDefinition = JOB_DEFINITION,
        arrayProperties= {"size": n},      # ← this is what makes it an array job
        containerOverrides={
            # Each element runs this inline command:
            # 1. Read the image prefix list from S3
            # 2. Pick the prefix at index = AWS_BATCH_JOB_ARRAY_INDEX
            # 3. Run generate_captions then embed_captions
            "command": [
                "bash", "-c",
                (
                    "IMAGE_PREFIX=$(python3 -c \""
                    "import boto3, json, os; "
                    "s3=boto3.client('s3'); "
                    "prefixes=json.loads(s3.get_object(Bucket=os.environ['S3_BUCKET'], "
                    "Key=os.environ['ARRAY_WORKER_KEY'])['Body'].read()); "
                    "idx=int(os.environ['AWS_BATCH_JOB_ARRAY_INDEX']); "
                    "print(prefixes[idx])\") && "
                    "IMAGE_BATCH_STEM=$(python3 -c \"import os; print(os.path.basename('$IMAGE_PREFIX'.rstrip('/')))\") && "
                    "S3_BUCKET=$S3_BUCKET IMAGE_PREFIX=$IMAGE_PREFIX BATCH_SIZE=8 "
                    "python /app/lessons/03-images-to-captions/generate_captions.py && "
                    "S3_BUCKET=$S3_BUCKET IMAGE_BATCH_STEM=$IMAGE_BATCH_STEM BATCH_SIZE=16 "
                    "python /app/lessons/04-captions-to-embeddings/embed_captions.py"
                )
            ],
            "environment": [
                {"name": "S3_BUCKET",        "value": S3_BUCKET},
                {"name": "S3_VECTOR_BUCKET", "value": S3_VECTOR_BUCKET},
                {"name": "S3_VECTOR_INDEX",  "value": S3_VECTOR_INDEX},
                {"name": "ARRAY_WORKER_KEY", "value": ARRAY_WORKER_KEY},
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
        help="S3 prefixes of image batches to process (already uploaded to S3)",
    )
    args = parser.parse_args()

    upload_image_prefix_list(args.image_prefixes)

    final_state = wait(submit_array(len(args.image_prefixes)))
    print(f"\n{'✅' if final_state == 'SUCCEEDED' else '❌'}  Array job {final_state}")
    print(f"Embeddings are in {S3_VECTOR_BUCKET}/{S3_VECTOR_INDEX}.")
