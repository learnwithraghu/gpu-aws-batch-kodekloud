# Lesson 03 — Theory

This lesson builds the image on your laptop. Batch does not see it until lesson 04 pushes to ECR.

## Why containers for GPU jobs

A GPU job needs a matching stack: NVIDIA drivers on the host, CUDA libraries, a PyTorch build that talks to that CUDA, and Python packages pinned to versions that work together.

A container packages the app-side stack (CUDA runtime libraries, PyTorch, transformers, your scripts) so every Batch run starts from the same filesystem. The host still needs the NVIDIA ECS AMI (lesson 01 / 07). The container is not a substitute for the driver on the instance.

## Base image choice

This course starts from `pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime`. That base already includes a CUDA-enabled PyTorch.

Building CUDA and PyTorch from scratch in a Dockerfile is possible and slow. For teaching batch inference, a maintained PyTorch+CUDA image is the practical default. You add only `requirements-gpu.txt` and the two lesson 02 files.

## Dependency pinning

`transformers==4.46.3` is pinned on purpose. Newer `transformers` releases expect newer PyTorch. On this 2.1 base they fail at import or disable themselves. The GPU job then exits before it describes a photo.

Pinning is not pedantry. It is how you keep last week’s working image from breaking when a fresh `pip install` resolves to a different major version.

## Build context and `.dockerignore`

`docker build` sends a **build context** (files under the path you pass, here the repo root) to the daemon. Larger context means slower builds and a higher chance of copying secrets.

`.dockerignore` drops `.env`, `.git`, helpers you do not need in the image, and so on. Credentials stay in `~/.aws/` via `aws configure`, never in the image layers.

## Architecture: `linux/amd64`

Batch’s `g4dn.xlarge` is x86_64. Apple Silicon laptops default to `arm64` images unless you say otherwise.

`docker build --platform linux/amd64` produces an image the GPU instance can run. An arm64 image can push to ECR cleanly and then fail when the instance pulls it. The failure shows up at job time, not at push time.

## Layer caching

Docker builds in layers. A typical order is: base → install requirements → copy app code.

If only `describe_items.py` changes, Docker reuses the heavy pip layer and rebuilds the thin copy layers. If `requirements-gpu.txt` changes, pip runs again. That is why first builds take 15–25 minutes and later code-only rebuilds are much faster.

## Local tag vs remote truth

`docker images` showing `gpu-teaching:latest` means your laptop has a tag. AWS Batch does not pull from your laptop.

Until lesson 04 pushes that tag to ECR, the job definition still points at whatever `:latest` (or digest) already lives in the registry — which may be yesterday’s scripts. Always treat “built locally” and “what Batch will run” as two different facts until the push succeeds.
