"""
Lesson 03 · Step 00 — register-job-def
Register the course job definition that points AWS Batch at the Docker
image we pushed to ECR in lesson 00.

This is the glue between "image exists in ECR" and "Batch can run it":
a job definition is where you declare the image, the resources the
container needs (1 GPU here), and default environment variables.

Run:  python main.py
"""
import os

import boto3
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../../.env"))

ECR_IMAGE_URI  = os.environ["ECR_IMAGE_URI"]
S3_BUCKET      = os.environ["S3_BUCKET"]
S3_CSV_BUCKET  = os.environ.get("S3_CSV_BUCKET", S3_BUCKET)
JOB_DEFINITION = os.environ["BATCH_JOB_DEFINITION"]
REGION         = os.environ.get("AWS_DEFAULT_REGION", "ap-northeast-1")

batch = boto3.client("batch", region_name=REGION)

# What the container runs by default (steps 02/04 override the command at
# submit time — this default just proves the image + GPU work).
DEFAULT_COMMAND = [
    "python", "-c",
    "import torch; print('CUDA:', torch.cuda.is_available(), "
    "'|', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'no GPU')",
]

CONTAINER_PROPERTIES = {
    "image": ECR_IMAGE_URI,
    "resourceRequirements": [
        {"type": "VCPU",   "value": "4"},
        {"type": "MEMORY", "value": "16384"},
        {"type": "GPU",    "value": "1"},
    ],
    "environment": [
        {"name": "S3_BUCKET",     "value": S3_BUCKET},
        {"name": "S3_CSV_BUCKET", "value": S3_CSV_BUCKET},
    ],
    "command": DEFAULT_COMMAND,
}


def find_active() -> dict | None:
    """Highest active revision of JOB_DEFINITION, or None."""
    resp = batch.describe_job_definitions(jobDefinitionName=JOB_DEFINITION, status="ACTIVE")
    revs = resp["jobDefinitions"]
    return max(revs, key=lambda j: j["revision"]) if revs else None


existing = find_active()
if existing and existing["containerProperties"]["image"] == ECR_IMAGE_URI:
    print(f"✅ {JOB_DEFINITION}:{existing['revision']} already points at our image — nothing to do")
else:
    if existing:
        print(f"Image changed → registering a new revision "
              f"(was {existing['containerProperties']['image']})")
    resp = batch.register_job_definition(
        jobDefinitionName=JOB_DEFINITION,
        type="container",
        containerProperties=CONTAINER_PROPERTIES,
    )
    existing = resp
    print(f"Registered {resp['jobDefinitionArn']}")

print(f"\nJob definition : {existing['jobDefinitionArn']}")
print(f"Image          : {existing['containerProperties']['image']}")
print("Resources      : 4 vCPU · 16 GiB · 1 GPU (g4dn.xlarge)")
print("\nNext: caption one image   python ../02-caption-one-image/main.py")
