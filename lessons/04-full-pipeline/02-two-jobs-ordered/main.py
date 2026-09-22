"""
Lesson 04 · Step 02 — two-jobs-ordered
The SAME pipeline as step 01, with ONE line added: dependsOn. Job 2 now
waits for Job 1 to SUCCEED. If Job 1 fails, Job 2 is cancelled automatically.

Run:  python main.py [--batch-stem pipeline-demo]
"""
import argparse
import glob
import os
import time

import boto3
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../../.env"))

S3_BUCKET      = os.environ["S3_BUCKET"]
JOB_QUEUE      = os.environ["BATCH_JOB_QUEUE"]
JOB_DEFINITION = os.environ["BATCH_JOB_DEFINITION"]
REGION         = os.environ.get("AWS_DEFAULT_REGION", "ap-northeast-1")

s3    = boto3.client("s3",    region_name=REGION)
batch = boto3.client("batch", region_name=REGION)

parser = argparse.ArgumentParser()
parser.add_argument("--images-dir",
                    default=os.path.join(os.path.dirname(__file__), "..", "assets", "images"))
parser.add_argument("--batch-stem", default="pipeline-demo")
args = parser.parse_args()

# 1. Upload images
image_paths = sorted(
    p for ext in ("*.jpg", "*.jpeg", "*.png")
    for p in glob.glob(os.path.join(args.images_dir, ext))
)
if not image_paths:
    raise FileNotFoundError(f"No images found in {args.images_dir}")

image_prefix = f"images/{args.batch_stem}"
for path in image_paths:
    s3.upload_file(path, S3_BUCKET, f"{image_prefix}/{os.path.basename(path)}")
print(f"Uploaded {len(image_paths)} images to s3://{S3_BUCKET}/{image_prefix}/")

# 2. Job 1: caption the batch
job1 = batch.submit_job(
    jobName=f"ordered-caption-{args.batch_stem}",
    jobQueue=JOB_QUEUE,
    jobDefinition=JOB_DEFINITION,
    containerOverrides={
        "command": ["python",
                    "/app/lessons/03-images-to-captions/03-caption-whole-batch/generate_captions.py"],
        "environment": [
            {"name": "S3_BUCKET",    "value": S3_BUCKET},
            {"name": "IMAGE_PREFIX", "value": image_prefix},
            {"name": "BATCH_SIZE",   "value": "8"},
        ],
    },
)
job1_id = job1["jobId"]
print(f"Submitted Job 1 (caption): {job1_id}")

# 3. Job 2: verify — THE FIX is the dependsOn line below
job2 = batch.submit_job(
    jobName=f"ordered-verify-{args.batch_stem}",
    jobQueue=JOB_QUEUE,
    jobDefinition=JOB_DEFINITION,
    dependsOn=[{"jobId": job1_id, "type": "N_TO_N"}],   # ← the only change from step 01
    containerOverrides={
        "command": ["python", "/app/lessons/04-full-pipeline/03-the-verify-job/verify_captions.py"],
        "environment": [
            {"name": "S3_BUCKET",    "value": S3_BUCKET},
            {"name": "IMAGE_PREFIX", "value": image_prefix},
        ],
    },
)
job2_id = job2["jobId"]
print(f"Submitted Job 2 (verify) : {job2_id}   (waiting for Job 1)")

# 4. Poll both jobs
terminal = {"SUCCEEDED", "FAILED"}
print("\nPolling every 15 s ...")
states = {}
while True:
    jobs = batch.describe_jobs(jobs=[job1_id, job2_id])["jobs"]
    states = {j["jobId"]: j["status"] for j in jobs}
    print(f"  Job1 (caption): {states[job1_id]}  |  Job2 (verify): {states[job2_id]}")
    if states[job1_id] in terminal and states[job2_id] in terminal:
        break
    time.sleep(15)

print(f"\nJob 1 (caption): {'✅' if states[job1_id] == 'SUCCEEDED' else '❌'}  {states[job1_id]}")
print(f"Job 2 (verify) : {'✅' if states[job2_id] == 'SUCCEEDED' else '❌'}  {states[job2_id]}")

if states[job1_id] == "SUCCEEDED" and states[job2_id] == "SUCCEEDED":
    print(f"\nCaptions : s3://{S3_BUCKET}/captions/{args.batch_stem}/captions.csv")
    print(f"Marker   : s3://{S3_BUCKET}/captions/{args.batch_stem}/_VERIFIED")
