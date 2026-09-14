"""
Lesson 04 — submit_job.py
Runs LOCALLY. Submits the CLIP embedding job to AWS Batch.

Assumes lesson 03 already ran and frames are in S3 at frames/<video_stem>/

Usage:
    python submit_job.py [--video-stem sample]
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
REGION         = os.environ.get("AWS_DEFAULT_REGION", "ap-northeast-1")

batch = boto3.client("batch", region_name=REGION)


def submit(video_stem: str) -> str:
    response = batch.submit_job(
        jobName      = f"lesson-04-embed-{video_stem}",
        jobQueue     = JOB_QUEUE,
        jobDefinition= JOB_DEFINITION,
        containerOverrides={
            "command": ["python", "/app/lessons/04-frames-to-embeddings/embed_frames.py"],
            "environment": [
                {"name": "S3_BUCKET",   "value": S3_BUCKET},
                {"name": "VIDEO_STEM",  "value": video_stem},
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
    parser.add_argument("--video-stem", default="sample", help="Video name without extension")
    args = parser.parse_args()

    job_id      = submit(args.video_stem)
    final_state = wait(job_id)

    print(f"\n{'✅' if final_state == 'SUCCEEDED' else '❌'}  Job {final_state}")
    print(f"Embeddings at: s3://{S3_BUCKET}/embeddings/{args.video_stem}/")
