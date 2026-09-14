"""
Lesson 02 — submit_job.py
Runs LOCALLY. Submits job.py to AWS Batch and waits for it to finish.

Usage:
    python submit_job.py

Reads from the repo root .env file (AWS credentials + Batch config).
"""
import time
import boto3
from dotenv import load_dotenv
import os

# Load secrets from the root .env file (two levels up from this script)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

JOB_QUEUE      = os.environ["BATCH_JOB_QUEUE"]
JOB_DEFINITION = os.environ["BATCH_JOB_DEFINITION"]
REGION         = os.environ.get("AWS_DEFAULT_REGION", "ap-northeast-1")

batch = boto3.client("batch", region_name=REGION)


def submit() -> str:
    """Submit the job and return the job ID."""
    response = batch.submit_job(
        jobName      = "lesson-02-hello-gpu",
        jobQueue     = JOB_QUEUE,
        jobDefinition= JOB_DEFINITION,
        containerOverrides={
            # Tell the container which script to run
            "command": ["python", "/app/lessons/02-first-batch-job/job.py"]
        },
    )
    job_id = response["jobId"]
    print(f"Submitted  job id : {job_id}")
    return job_id


def wait(job_id: str) -> str:
    """Poll every 10 seconds until the job reaches a terminal state."""
    terminal_states = {"SUCCEEDED", "FAILED"}
    print("Waiting for job to complete (polling every 10 s) ...")

    while True:
        resp  = batch.describe_jobs(jobs=[job_id])
        job   = resp["jobs"][0]
        state = job["status"]
        print(f"  Status: {state}")

        if state in terminal_states:
            return state
        time.sleep(10)


def print_logs_link(job_id: str):
    """Print a direct CloudWatch link so you can read the GPU output."""
    resp       = batch.describe_jobs(jobs=[job_id])
    log_stream = resp["jobs"][0].get("container", {}).get("logStreamName", "")
    if log_stream:
        url = (
            f"https://{REGION}.console.aws.amazon.com/cloudwatch/home"
            f"?region={REGION}#logsV2:log-groups/log-group/"
            f"%2Faws%2Fbatch%2Fjob/log-events/{log_stream.replace('/', '%2F')}"
        )
        print(f"\nCloudWatch logs:\n  {url}")
    else:
        print("\n(log stream not found — check the AWS Console)")


if __name__ == "__main__":
    job_id = submit()
    final_state = wait(job_id)

    if final_state == "SUCCEEDED":
        print("\n✅  Job SUCCEEDED")
    else:
        print("\n❌  Job FAILED — check CloudWatch logs")

    print_logs_link(job_id)
