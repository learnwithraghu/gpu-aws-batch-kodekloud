# Lesson 03 — Build the image locally

AWS Batch runs a container image. This lesson builds that image on your machine and stops there. ECR is the next lesson.

Theory reading: [`theory.md`](theory.md).

Work from the repo root. Docker Desktop must be running.

## What the Dockerfile does

The [Dockerfile](../../Dockerfile) starts from `pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime`, installs [`requirements-gpu.txt`](../../requirements-gpu.txt), and copies both lesson 02 files:

```
COPY lessons/02-the-container-program/photos.py /app/photos.py
COPY lessons/02-the-container-program/describe_items.py /app/describe_items.py
```

Batch runs `describe_items.py`. That file imports `photos.py` from the same `/app` folder.

`transformers` is pinned to `4.46.3`. Newer releases refuse to run on this PyTorch 2.1 base, and the GPU job exits before it describes a photo.

## Build

```bash
docker build --platform linux/amd64 -t gpu-teaching:latest .
```

`--platform linux/amd64` matters on Apple Silicon. Batch’s `g4dn.xlarge` is x86_64. An arm64 image pushes cleanly and then fails on the instance.

The first build downloads the CUDA base and installs pip packages. Plan on 15–25 minutes. A later build reuses Docker’s cache unless you change the Dockerfile, `requirements-gpu.txt`, `photos.py`, or `describe_items.py`.

## Check

```bash
docker images gpu-teaching
```

You should see a local tag `gpu-teaching:latest`, several gigabytes. That tag is only on your laptop. Lesson 04 creates the ECR repository and pushes it.
