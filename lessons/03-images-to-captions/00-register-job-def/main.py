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
    # Memory stays below the g4dn.xlarge's 16 GiB: ECS registers usable
    # memory slightly under the instance total (OS + agent overhead), so a
    # job asking for the full 16384 MiB can never be placed
    # (MISCONFIGURATION:JOB_RESOURCE_REQUIREMENT).
    "resourceRequirements": [
        {"type": "VCPU",   "value": "4"},
        {"type": "MEMORY", "value": "12288"},
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


def matches(existing: dict) -> bool:
    """True if the active revision already has exactly the desired config."""
    c = existing["containerProperties"]
    req  = sorted(c.get("resourceRequirements", []), key=lambda r: r["type"])
    want = sorted(CONTAINER_PROPERTIES["resourceRequirements"], key=lambda r: r["type"])
    return (
        c.get("image") == CONTAINER_PROPERTIES["image"]
        and req == want
        and c.get("environment", []) == CONTAINER_PROPERTIES["environment"]
        and c.get("command", []) == CONTAINER_PROPERTIES["command"]
    )


existing = find_active()
if existing and matches(existing):
    print(f"✅ {JOB_DEFINITION}:{existing['revision']} already matches — nothing to do")
else:
    if existing:
        print("Config changed → registering a new revision")
    resp = batch.register_job_definition(
        jobDefinitionName=JOB_DEFINITION,
        type="container",
        containerProperties=CONTAINER_PROPERTIES,
    )
    print(f"Registered {resp['jobDefinitionArn']}")
    existing = find_active()   # describe shape includes containerProperties

print(f"\nJob definition : {existing['jobDefinitionArn']}")
print(f"Image          : {existing['containerProperties']['image']}")
print("Resources      : 4 vCPU · 12 GiB · 1 GPU (g4dn.xlarge)")
print("\nNext: caption one image   python ../02-caption-one-image/main.py")
