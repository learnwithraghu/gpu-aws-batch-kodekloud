"""
Lesson 06 — run_pipeline.py
Runs LOCALLY. Submits the full images → captions → embeddings pipeline as two
chained Batch jobs.

Job 1: generate_captions   (from lesson 03)
Job 2: embed_captions      (from lesson 04, runs only after job 1 SUCCEEDS)

Usage:
    python run_pipeline.py --images-dir assets/images

The images are uploaded to S3 first, then both jobs are submitted to Batch.
"""
import argparse
import glob
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


def upload_images(local_dir: str, batch_stem: str) -> str:
    """Upload every image in local_dir to S3. Returns the S3 prefix used."""
    image_paths = sorted(
        p for ext in ("*.jpg", "*.jpeg", "*.png") for p in glob.glob(os.path.join(local_dir, ext))
    )
    if not image_paths:
        raise FileNotFoundError(f"No .jpg/.jpeg/.png images found in {local_dir}")

    prefix = f"images/{batch_stem}"
    for path in image_paths:
        s3_key = f"{prefix}/{os.path.basename(path)}"
        print(f"Uploading {path} → s3://{S3_BUCKET}/{s3_key} ...")
        s3.upload_file(path, S3_BUCKET, s3_key)
    print(f"  Uploaded {len(image_paths)} images.")
    return prefix


def submit_pipeline(image_prefix: str, batch_stem: str) -> tuple[str, str]:
    """Submit both jobs. Returns (job1_id, job2_id)."""

    # ── Job 1: generate captions ─────────────────────────────────────────────
    job1 = batch.submit_job(
        jobName      = f"pipeline-caption-{batch_stem}",
        jobQueue     = JOB_QUEUE,
        jobDefinition= JOB_DEFINITION,
        containerOverrides={
            "command": ["python", "/app/lessons/03-images-to-captions/generate_captions.py"],
            "environment": [
                {"name": "S3_BUCKET",     "value": S3_BUCKET},
                {"name": "IMAGE_PREFIX",  "value": image_prefix},
                {"name": "BATCH_SIZE",    "value": "8"},
            ],
        },
    )
    job1_id = job1["jobId"]
    print(f"Submitted Job 1 (caption): {job1_id}")

    # ── Job 2: embed captions — only starts after Job 1 SUCCEEDS ────────────
    job2 = batch.submit_job(
        jobName      = f"pipeline-embed-{batch_stem}",
        jobQueue     = JOB_QUEUE,
        jobDefinition= JOB_DEFINITION,
        dependsOn    = [{"jobId": job1_id, "type": "N_TO_N"}],   # ← the key line
        containerOverrides={
            "command": ["python", "/app/lessons/04-captions-to-embeddings/embed_captions.py"],
            "environment": [
                {"name": "S3_BUCKET",  "value": S3_BUCKET},
                {"name": "S3_VECTOR_BUCKET", "value": S3_VECTOR_BUCKET},
                {"name": "S3_VECTOR_INDEX", "value": S3_VECTOR_INDEX},
                {"name": "IMAGE_BATCH_STEM", "value": batch_stem},
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
        print(f"  Job1 (caption): {states[job1_id]}  |  Job2 (embed): {states[job2_id]}")

        if states[job1_id] in terminal and states[job2_id] in terminal:
            break
        time.sleep(15)

    return states[job1_id], states[job2_id]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--images-dir", default="assets/images", help="Local folder of images to process")
    parser.add_argument("--batch-stem", default="sample",        help="Name for this image batch (used as the S3 prefix)")
    args = parser.parse_args()

    image_prefix      = upload_images(args.images_dir, args.batch_stem)
    job1_id, job2_id  = submit_pipeline(image_prefix, args.batch_stem)
    state1, state2    = wait_for_jobs(job1_id, job2_id)

    ok1 = state1 == "SUCCEEDED"
    ok2 = state2 == "SUCCEEDED"

    print(f"\nJob 1 (caption): {'✅' if ok1 else '❌'}  {state1}")
    print(f"Job 2 (embed)  : {'✅' if ok2 else '❌'}  {state2}")

    if ok1 and ok2:
        print(f"\nEmbeddings ready in {S3_VECTOR_BUCKET}/{S3_VECTOR_INDEX}")
