# Lesson 05 — Register the job

The job definition tells Batch which image to run and how much GPU, CPU, and memory to reserve. [`register_job_def.py`](../../register_job_def.py) creates it, or leaves it alone when it already matches.

## What gets registered

| Setting | Value |
|---------|--------|
| Image | `ECR_IMAGE_URI` from `.env` |
| vCPU | 4 |
| Memory | 12288 MiB |
| GPU | 1 |
| Job role | `BATCH_JOB_ROLE_ARN` |

Memory stays at 12288 MiB because a `g4dn.xlarge` cannot place a job that asks for the full 16384 MiB. The job role is how the container reads the images bucket and writes the CSV. The EC2 instance role does not have S3 access.

The default command only checks that CUDA is visible. `submit_job.py` replaces it with `describe_items.py`.

## The command

```bash
python register_job_def.py
```

Needs `boto3` and `python-dotenv` (`uv run --with boto3 --with python-dotenv python register_job_def.py` works the same way).

## What "already matches" means

A second run prints `already matches` and does not register a new revision. A new revision appears only when the image, resources, environment, command, or role changed.

## Which revision to use

Use revision `:3` or later of `gpu-teaching-caption-job`.

- `:1` asks for 16384 MiB and never leaves `RUNNABLE`.
- `:2` has the right memory and no job role, so S3 calls fail with `AccessDenied`.

Submit by name. Batch uses the highest active revision.
