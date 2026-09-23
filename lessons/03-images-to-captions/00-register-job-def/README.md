# Step 00 — Register the job definition

A Batch **job definition** points AWS Batch at a container image and declares
what resources the container needs. This one-time step wires the image we
pushed to ECR in lesson 00 to the GPU queue: **4 vCPU · 12 GiB · 1 GPU**
(a g4dn.xlarge — memory stays under the instance's 16 GiB because the OS
and ECS agent reserve some), with the course S3 buckets as default
environment variables.

Idempotent — run it again and it reuses the existing registration; if the
`ECR_IMAGE_URI` in `.env` or the resource config has changed, it registers
a new revision instead.

**Run:** `python main.py`

**Expected:** the job definition ARN, e.g.
`arn:aws:batch:<region>:<account>:job-definition/gpu-teaching-caption-job:1`
