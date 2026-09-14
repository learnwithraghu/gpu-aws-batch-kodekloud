"""
Lesson 07 — submit_array_job.py
Runs LOCALLY. Processes multiple videos in parallel using a Batch array job.

Each array element reads its index from AWS_BATCH_JOB_ARRAY_INDEX, looks up
the corresponding video key in a JSON list stored in S3, and runs the full
extract → embed pipeline.

Usage:
    # First upload all videos to S3:
    aws s3 cp videos/ s3://<bucket>/videos/ --recursive

    # Then submit an array job (one element per video):
    python submit_array_job.py --video-keys videos/clip1.mp4 videos/clip2.mp4 videos/clip3.mp4
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

# The array worker script (embedded inline to keep this lesson self-contained)
ARRAY_WORKER_KEY = "config/array_video_keys.json"


def upload_video_list(video_keys: list[str]):
    """Save the list of video S3 keys to S3 so each array element can read it."""
    body = json.dumps(video_keys).encode()
    s3.put_object(Bucket=S3_BUCKET, Key=ARRAY_WORKER_KEY, Body=body)
    print(f"Saved {len(video_keys)} video keys to s3://{S3_BUCKET}/{ARRAY_WORKER_KEY}")


def submit_array(n: int) -> str:
    """Submit one array job with n elements. Returns the array job ID."""
    response = batch.submit_job(
        jobName       = "lesson-07-array-pipeline",
        jobQueue      = JOB_QUEUE,
        jobDefinition = JOB_DEFINITION,
        arrayProperties= {"size": n},      # ← this is what makes it an array job
        containerOverrides={
            # Each element runs this inline command:
            # 1. Read the video key list from S3
            # 2. Pick the key at index = AWS_BATCH_JOB_ARRAY_INDEX
            # 3. Run extract_frames then embed_frames
            "command": [
                "bash", "-c",
                (
                    "pip install awscli -q && "
                    "VIDEO_KEY=$(python3 -c \""
                    "import boto3, json, os; "
                    "s3=boto3.client('s3'); "
                    "keys=json.loads(s3.get_object(Bucket=os.environ['S3_BUCKET'], "
                    "Key=os.environ['ARRAY_WORKER_KEY'])['Body'].read()); "
                    "idx=int(os.environ['AWS_BATCH_JOB_ARRAY_INDEX']); "
                    "print(keys[idx])\") && "
                    "VIDEO_STEM=$(python3 -c \"import os, sys; print(os.path.splitext(os.path.basename('$VIDEO_KEY'))[0])\") && "
                    "S3_BUCKET=$S3_BUCKET VIDEO_KEY=$VIDEO_KEY EVERY_N=30 "
                    "python /app/lessons/03-video-to-frames/extract_frames.py && "
                    "S3_BUCKET=$S3_BUCKET VIDEO_STEM=$VIDEO_STEM BATCH_SIZE=16 "
                    "python /app/lessons/04-frames-to-embeddings/embed_frames.py"
                )
            ],
            "environment": [
                {"name": "S3_BUCKET",        "value": S3_BUCKET},
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
        "--video-keys", nargs="+",
        default=["videos/sample.mp4"],
        help="S3 keys of videos to process (already uploaded to S3)",
    )
    args = parser.parse_args()

    upload_video_list(args.video_keys)

    final_state = wait(submit_array(len(args.video_keys)))
    print(f"\n{'✅' if final_state == 'SUCCEEDED' else '❌'}  Array job {final_state}")
    print("Check S3 under embeddings/ for results.")
