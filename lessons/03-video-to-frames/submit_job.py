"""
Lesson 03 — submit_job.py
Runs LOCALLY. Uploads the sample video to S3, then submits the
frame-extraction job to AWS Batch.

Usage:
    python submit_job.py [--video path/to/video.mp4] [--every-n 30]
"""
import argparse
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


def upload_video(local_path: str) -> str:
    """Upload the video to S3 and return its S3 key."""
    s3_key = f"videos/{os.path.basename(local_path)}"
    print(f"Uploading {local_path} → s3://{S3_BUCKET}/{s3_key} ...")
    s3.upload_file(local_path, S3_BUCKET, s3_key)
    print("  Done.")
    return s3_key


def submit(video_key: str, every_n: int) -> str:
    response = batch.submit_job(
        jobName      = "lesson-03-extract-frames",
        jobQueue     = JOB_QUEUE,
        jobDefinition= JOB_DEFINITION,
        containerOverrides={
            "command": ["python", "/app/lessons/03-video-to-frames/extract_frames.py"],
            # Pass configuration as environment variables
            "environment": [
                {"name": "S3_BUCKET",  "value": S3_BUCKET},
                {"name": "VIDEO_KEY",  "value": video_key},
                {"name": "EVERY_N",    "value": str(every_n)},
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
    parser.add_argument("--video",   default="assets/sample.mp4", help="Local video file to upload")
    parser.add_argument("--every-n", type=int, default=30,        help="Extract 1 frame every N frames")
    args = parser.parse_args()

    video_key   = upload_video(args.video)
    job_id      = submit(video_key, args.every_n)
    final_state = wait(job_id)

    print(f"\n{'✅' if final_state == 'SUCCEEDED' else '❌'}  Job {final_state}")
    print(f"Frames are at: s3://{S3_BUCKET}/frames/{os.path.splitext(os.path.basename(args.video))[0]}/")
