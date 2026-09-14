"""
Lesson 06 — run_pipeline.py
Runs LOCALLY. Submits the full video → embeddings pipeline as two chained Batch jobs.

Job 1: extract_frames   (from lesson 03)
Job 2: embed_frames     (from lesson 04, runs only after job 1 SUCCEEDS)

Usage:
    python run_pipeline.py --video assets/sample.mp4

The video is uploaded to S3 first, then both jobs are submitted to Batch.
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


def upload_video(local_path: str) -> tuple[str, str]:
    """Upload video to S3. Returns (s3_key, video_stem)."""
    video_stem = os.path.splitext(os.path.basename(local_path))[0]
    s3_key     = f"videos/{os.path.basename(local_path)}"
    print(f"Uploading {local_path} → s3://{S3_BUCKET}/{s3_key} ...")
    s3.upload_file(local_path, S3_BUCKET, s3_key)
    return s3_key, video_stem


def submit_pipeline(video_key: str, video_stem: str) -> tuple[str, str]:
    """Submit both jobs. Returns (job1_id, job2_id)."""

    # ── Job 1: extract frames ────────────────────────────────────────────────
    job1 = batch.submit_job(
        jobName      = f"pipeline-extract-{video_stem}",
        jobQueue     = JOB_QUEUE,
        jobDefinition= JOB_DEFINITION,
        containerOverrides={
            "command": ["python", "/app/lessons/03-video-to-frames/extract_frames.py"],
            "environment": [
                {"name": "S3_BUCKET",  "value": S3_BUCKET},
                {"name": "VIDEO_KEY",  "value": video_key},
                {"name": "EVERY_N",    "value": "30"},
            ],
        },
    )
    job1_id = job1["jobId"]
    print(f"Submitted Job 1 (extract): {job1_id}")

    # ── Job 2: embed frames — only starts after Job 1 SUCCEEDS ──────────────
    job2 = batch.submit_job(
        jobName      = f"pipeline-embed-{video_stem}",
        jobQueue     = JOB_QUEUE,
        jobDefinition= JOB_DEFINITION,
        dependsOn    = [{"jobId": job1_id, "type": "N_TO_N"}],   # ← the key line
        containerOverrides={
            "command": ["python", "/app/lessons/04-frames-to-embeddings/embed_frames.py"],
            "environment": [
                {"name": "S3_BUCKET",  "value": S3_BUCKET},
                {"name": "VIDEO_STEM", "value": video_stem},
                {"name": "BATCH_SIZE", "value": "16"},
            ],
        },
    )
    job2_id = job2["jobId"]
    print(f"Submitted Job 2 (embed)  : {job2_id}  (waiting for Job 1)")
    return job1_id, job2_id


def wait_for_jobs(job1_id: str, job2_id: str):
    """Poll both jobs until both reach a terminal state."""
    terminal = {"SUCCEEDED", "FAILED"}
    states   = {}

    print("\nPolling every 15 s ...")
    while True:
        jobs   = batch.describe_jobs(jobs=[job1_id, job2_id])["jobs"]
        states = {j["jobId"]: j["status"] for j in jobs}
        print(f"  Job1 (extract): {states[job1_id]}  |  Job2 (embed): {states[job2_id]}")

        if states[job1_id] in terminal and states[job2_id] in terminal:
            break
        time.sleep(15)

    return states[job1_id], states[job2_id]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", default="assets/sample.mp4", help="Local video to process")
    args = parser.parse_args()

    video_key, video_stem = upload_video(args.video)
    job1_id, job2_id      = submit_pipeline(video_key, video_stem)
    state1, state2        = wait_for_jobs(job1_id, job2_id)

    ok1 = state1 == "SUCCEEDED"
    ok2 = state2 == "SUCCEEDED"

    print(f"\nJob 1 (extract): {'✅' if ok1 else '❌'}  {state1}")
    print(f"Job 2 (embed)  : {'✅' if ok2 else '❌'}  {state2}")

    if ok1 and ok2:
        print(f"\nEmbeddings ready at: s3://{S3_BUCKET}/embeddings/{video_stem}/")
