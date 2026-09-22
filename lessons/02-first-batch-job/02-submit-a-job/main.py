"""
Lesson 02 · Step 02 — submit-a-job
Submit job.py (step 01) to AWS Batch. Print the job ID — that's all.

Run:  python main.py
Then: python ../03-watch-until-done/main.py --job-id <id printed here>
"""
import argparse
import os

import boto3
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../../.env"))

JOB_QUEUE      = os.environ["BATCH_JOB_QUEUE"]
JOB_DEFINITION = os.environ["BATCH_JOB_DEFINITION"]
REGION         = os.environ.get("AWS_DEFAULT_REGION", "ap-northeast-1")

batch = boto3.client("batch", region_name=REGION)

parser = argparse.ArgumentParser(description="Submit the GPU check job to Batch.")
parser.add_argument("--name", default="lesson-02-gpu-check", help="Job name")
args = parser.parse_args()

response = batch.submit_job(
    jobName=args.name,
    jobQueue=JOB_QUEUE,
    jobDefinition=JOB_DEFINITION,
    containerOverrides={
        "command": ["python", "/app/lessons/02-first-batch-job/01-the-container-script/job.py"],
    },
)

print(f"Submitted job : {response['jobId']}")
print(f"Job name      : {args.name}")
print(f"Watch it      : python ../03-watch-until-done/main.py --job-id {response['jobId']}")
