# Lesson 04 — The image

AWS Batch runs a container image from ECR. It does not run `describe_items.py` from your laptop.

## What is copied in

The [Dockerfile](../../Dockerfile) starts from `pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime`, installs [`requirements-gpu.txt`](../../requirements-gpu.txt), and copies one script:

```
COPY describe_items.py /app/describe_items.py
```

That path is what `submit_job.py` executes: `python /app/describe_items.py`.

## What Batch runs

The job definition points at `ECR_IMAGE_URI` in `.env`, the `:latest` tag of `gpu-teaching`. A job started after a push pulls that tag. A job started before the push still has the previous image.

## When to rebuild

Rebuild after any change to the Dockerfile, `requirements-gpu.txt`, or `describe_items.py`:

```bash
bash helpers/push_ecr_image.sh
```

The first build on a machine takes a while (CUDA base, pip, push). Later builds reuse Docker's cache. The script writes `ECR_IMAGE_URI` back to `.env`.

You do not need to rebuild to upload new photos. New photos are read from S3 at job time.
