# Lesson 08 — Theory

Submit is the moment data, image, and Batch meet. Most debugging time lives in the statuses below.

## Submit vs run

`submit-job` accepts the request and returns a job id. That does not mean a GPU is running yet.

Batch places the job when the queue’s compute environment can provide the vCPU, memory, and GPU the definition asks for. Acceptance is cheap. Capacity is the scarce part — especially for Spot GPUs.

## Container overrides

Overrides change the **this run** without registering a new revision:

- `command` — replace the CUDA check with `python /app/describe_items.py`
- `environment` — buckets, `IMAGE_PREFIX`, `BATCH_SIZE`

Use overrides for per-folder config. Use a new job-definition revision when the image URI, GPU count, memory, or job role should change for everyone.

## Status path

Typical happy path:

`SUBMITTED` → `RUNNABLE` → `STARTING` → `RUNNING` → `SUCCEEDED`

| Status | Meaning |
|--------|---------|
| `RUNNABLE` | Waiting for capacity or still being placed |
| `STARTING` | Instance/agent bringing the container up |
| `RUNNING` | Your process is executing |
| `FAILED` | Process or infrastructure gave up |

`SUCCEEDED` means the container exited 0. It does not by itself prove the CSV schema is perfect — lesson 09 checks the object.

## Diagnosing stuck `RUNNABLE`

Long `RUNNABLE` is usually one of:

- No Spot capacity / quota for `g4dn`
- Memory or GPU request that cannot place (`16384` MiB classic mistake)
- Compute environment `INVALID` or disabled
- Queue bound to the wrong CE

**No CloudWatch `/aws/batch/job` stream while `RUNNABLE`.** The container has not started, so prints inside `describe_items.py` cannot appear. Check `statusReason` on the job and the CE (`desiredvCpus`). Lesson 08’s wait step uses `helpers/watch_batch_job.sh`, which prints that hint after about two minutes. Switching to the on-demand queue is the course’s capacity escape hatch — after you understand it is capacity, not a bad Python import.

## Cold start costs

The first job on a fresh instance pays for:

1. EC2 boot
2. ECR pull of a multi‑GB image
3. First download of BLIP weights into the container

Later jobs on a still-warm instance skip some of that. A 2–5 minute “slow” first run is often cold start, not a hung model. Watch CloudWatch for progress lines from `describe_items.py`.

## Logs as source of truth

`FAILED` with exit code 1 needs logs. Stream names live under `/aws/batch/job`.

Status alone says “it died.” Logs say `AccessDenied`, CUDA false, missing module, or empty image list. Lesson 08’s `describe-jobs` query includes `logStreamName` so you can jump straight there.

## Cancel and resubmit

If you leave a Spot job `RUNNABLE` and also submit on-demand, you can get two runs when Spot suddenly appears — double cost and a race on the same CSV key.

Cancel the stuck job with a clear reason, then submit on the on-demand queue. One folder should have one active attempt unless you intentionally want parallelism (this course does not).
