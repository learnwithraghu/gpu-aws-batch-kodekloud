"""
Lesson 03 — submit_job.py
Runs LOCALLY. Uploads a folder of sample images to S3, then submits the
image-captioning job to AWS Batch.

Usage:
    python submit_job.py [--images-dir assets/images] [--batch-size 8]
"""
import argparse
import glob
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


def submit(image_prefix: str, batch_size: int) -> str:
    response = batch.submit_job(
        jobName      = "lesson-03-generate-captions",
        jobQueue     = JOB_QUEUE,
        jobDefinition= JOB_DEFINITION,
        containerOverrides={
            "command": ["python", "/app/lessons/03-images-to-captions/generate_captions.py"],
            # Pass configuration as environment variables
            "environment": [
                {"name": "S3_BUCKET",     "value": S3_BUCKET},
                {"name": "IMAGE_PREFIX",  "value": image_prefix},
                {"name": "BATCH_SIZE",    "value": str(batch_size)},
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
    parser.add_argument("--images-dir",  default="assets/images", help="Local folder of images to upload")
    parser.add_argument("--batch-stem",  default="sample",        help="Name for this image batch (used as the S3 prefix)")
    parser.add_argument("--batch-size",  type=int, default=8,     help="Images captioned per GPU batch")
    args = parser.parse_args()

    image_prefix = upload_images(args.images_dir, args.batch_stem)
    job_id       = submit(image_prefix, args.batch_size)
    final_state  = wait(job_id)

    print(f"\n{'✅' if final_state == 'SUCCEEDED' else '❌'}  Job {final_state}")
    print(f"Captions are at: s3://{S3_BUCKET}/captions/{args.batch_stem}/manifest.json")
