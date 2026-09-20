"""
Lesson 04 — submit_job.py
Runs LOCALLY. Submits the CLIP caption-embedding job to AWS Batch.

Assumes lesson 03 already ran and captions are in S3 at captions/<image_batch_stem>/

Usage:
    python submit_job.py [--batch-stem sample]
"""
import argparse
import os
import time
import boto3
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

JOB_QUEUE      = os.environ["BATCH_JOB_QUEUE"]
JOB_DEFINITION = os.environ["BATCH_JOB_DEFINITION"]
S3_BUCKET      = os.environ["S3_BUCKET"]
S3_VECTOR_BUCKET = os.environ["S3_VECTOR_BUCKET"]
S3_VECTOR_INDEX = os.environ["S3_VECTOR_INDEX"]
REGION         = os.environ.get("AWS_DEFAULT_REGION", "ap-northeast-1")

batch = boto3.client("batch", region_name=REGION)


def submit(batch_stem: str) -> str:
    response = batch.submit_job(
        jobName      = f"lesson-04-embed-{batch_stem}",
        jobQueue     = JOB_QUEUE,
        jobDefinition= JOB_DEFINITION,
        containerOverrides={
            "command": ["python", "/app/lessons/04-captions-to-embeddings/embed_captions.py"],
            "environment": [
                {"name": "S3_BUCKET",   "value": S3_BUCKET},
                {"name": "S3_VECTOR_BUCKET", "value": S3_VECTOR_BUCKET},
                {"name": "S3_VECTOR_INDEX", "value": S3_VECTOR_INDEX},
                {"name": "IMAGE_BATCH_STEM",  "value": batch_stem},
                {"name": "BATCH_SIZE",  "value": "16"},
            ],
        },
    )
    job_id = response["jobId"]
    print(f"Submitted  job id : {job_id}")
    return job_id


def wait(job_id: str) -> str:
    terminal = {"SUCCEEDED", "FAILED"}
    print("Polling every 10 s ...")
    while True:
        state = batch.describe_jobs(jobs=[job_id])["jobs"][0]["status"]
        print(f"  Status: {state}")
        if state in terminal:
            return state
        time.sleep(10)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-stem", default="sample", help="Image batch name without extension")
    args = parser.parse_args()

    job_id      = submit(args.batch_stem)
    final_state = wait(job_id)

    print(f"\n{'✅' if final_state == 'SUCCEEDED' else '❌'}  Job {final_state}")
    print(f"Embeddings stored in S3 Vectors index: {S3_VECTOR_INDEX}")
