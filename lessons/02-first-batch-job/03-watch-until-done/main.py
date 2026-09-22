"""
Lesson 02 · Step 03 — watch-until-done
Poll a Batch job every 10 seconds until it reaches SUCCEEDED or FAILED.

Run:  python main.py --job-id <id from step 02>
"""
import argparse
import time

import boto3
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../../.env"))

REGION = os.environ.get("AWS_DEFAULT_REGION", "ap-northeast-1")
batch = boto3.client("batch", region_name=REGION)

parser = argparse.ArgumentParser(description="Watch a Batch job until it finishes.")
parser.add_argument("--job-id", required=True, help="Batch job ID to watch")
args = parser.parse_args()

terminal = {"SUCCEEDED", "FAILED"}

print("Polling every 10 s ...")
while True:
    job = batch.describe_jobs(jobs=[args.job_id])["jobs"][0]
    status = job["status"]
    print(f"  Status: {status}")
    if status in terminal:
        break
    time.sleep(10)

print(f"\n{'✅' if status == 'SUCCEEDED' else '❌'}  Job {status}")
print("Logs: AWS Console → CloudWatch → Log groups → /aws/batch/job")
