"""Register the GPU job definition used by the food-catalog job.

Run:  python register_job_def.py
"""
import os

import boto3
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

ECR_IMAGE_URI = os.environ["ECR_IMAGE_URI"]
S3_BUCKET = os.environ["S3_BUCKET"]
S3_CSV_BUCKET = os.environ.get("S3_CSV_BUCKET", S3_BUCKET)
JOB_DEFINITION = os.environ["BATCH_JOB_DEFINITION"]
JOB_ROLE_ARN = os.environ["BATCH_JOB_ROLE_ARN"]
REGION = os.environ.get("AWS_DEFAULT_REGION", "ap-northeast-1")

batch = boto3.client("batch", region_name=REGION)

DEFAULT_COMMAND = [
    "python", "-c",
    "import torch; print('CUDA:', torch.cuda.is_available(), "
    "'|', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'no GPU')",
]

CONTAINER_PROPERTIES = {
    "image": ECR_IMAGE_URI,
    # Stay under the g4dn.xlarge's 16 GiB. ECS reserves some for the OS,
    # so 16384 MiB can never be placed.
    "resourceRequirements": [
        {"type": "VCPU", "value": "4"},
        {"type": "MEMORY", "value": "12288"},
        {"type": "GPU", "value": "1"},
    ],
    "environment": [
        {"name": "S3_BUCKET", "value": S3_BUCKET},
        {"name": "S3_CSV_BUCKET", "value": S3_CSV_BUCKET},
    ],
    "command": DEFAULT_COMMAND,
    "jobRoleArn": JOB_ROLE_ARN,
}


def find_active() -> dict | None:
    resp = batch.describe_job_definitions(jobDefinitionName=JOB_DEFINITION, status="ACTIVE")
    revs = resp["jobDefinitions"]
    return max(revs, key=lambda j: j["revision"]) if revs else None


def matches(existing: dict) -> bool:
    c = existing["containerProperties"]
    req = sorted(c.get("resourceRequirements", []), key=lambda r: r["type"])
    want = sorted(CONTAINER_PROPERTIES["resourceRequirements"], key=lambda r: r["type"])
    return (
        c.get("image") == CONTAINER_PROPERTIES["image"]
        and req == want
        and c.get("environment", []) == CONTAINER_PROPERTIES["environment"]
        and c.get("command", []) == CONTAINER_PROPERTIES["command"]
        and c.get("jobRoleArn") == CONTAINER_PROPERTIES["jobRoleArn"]
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
    existing = find_active()

print(f"\nJob definition : {existing['jobDefinitionArn']}")
print(f"Image          : {existing['containerProperties']['image']}")
print(f"Job role       : {existing['containerProperties'].get('jobRoleArn')}")
print("Resources      : 4 vCPU · 12 GiB · 1 GPU (g4dn.xlarge)")
print("\nNext: python submit_job.py --batch-stem sample")
