# Plan — Lesson 03 caption job

**Goal:** `04-submit-and-wait` → `SUCCEEDED` and `05-show-captions` prints one row
for `--batch-stem sample`.

Infra names: [`docs/aws-batch-setup.md`](docs/aws-batch-setup.md). Bucket/ECR URIs
live in local `.env` only.

---

## Done (2026-09-28)

- Image rebuilt with `transformers==4.46.3` (`requirements-gpu.txt`) and pushed to
  ECR `:latest` (verified `transformers 4.46.3` in the local tag).
- Job def `gpu-teaching-caption-job:2` (12288 MiB, 1 GPU) — use this revision.
- Docker helper fix: no empty-array `set -u` crash; macOS `sed -i` for `.env`.

---

## Next (in order)

### 1. Submit and wait

```bash
cd lessons/03-images-to-captions/04-submit-and-wait
uv run --with boto3 --with python-dotenv python main.py --batch-stem sample
```

Expect: SUBMITTED → RUNNABLE → STARTING → RUNNING → SUCCEEDED. First run downloads
BLIP weights (~1 GB) inside the container.

### 2. Show captions

```bash
cd lessons/03-images-to-captions/05-show-captions
uv run --with boto3 --with python-dotenv python main.py --batch-stem sample
```

### 3. If the job fails — logs, then one fix

```bash
aws batch describe-jobs --jobs <job-id> --region ap-northeast-1 \
  --query 'jobs[0].[status,statusReason,attempts[0].container.exitCode,attempts[0].container.logStreamName]'

aws logs get-log-events --log-group-name /aws/batch/job \
  --log-stream-name '<logStreamName>' --region ap-northeast-1
```

| Symptom | Action |
|---------|--------|
| Stuck `RUNNABLE` ~5+ min | Set `BATCH_JOB_QUEUE=gpu-teaching-gpu-smoke-queue-on-demand` in `.env`, resubmit |
| `AccessDenied` on S3 | Job def has no `jobRoleArn`; add S3 policy + re-register via `00-register-job-def` |
| HF 429 / model download error | Add `HF_TOKEN` to job env (do not commit) |
| `Disabling PyTorch` / BLIP ImportError | Re-run `bash helpers/push_ecr_image.sh`, confirm fresh ECR push |

---

## Rebuild image (only when Dockerfile, `requirements-gpu.txt`, or `lessons/` change)

```bash
bash helpers/push_ecr_image.sh
```

First build on a machine: ~15–25 min (CUDA base + pip + push). Keep **≥15 GB free
on the Mac data volume** and Docker disk **≥50 GB** — a full Docker VM plus a
~4 GB layer extract fails with `unexpected EOF` when disk is tight.

---

## Out of scope

- Recreate CEs/queues or job def `:1` (16384 MiB).
- Commit `.env`, account IDs, or ARNs.
