# Video 000 — From S3 Input to GPU Job: Following the Execution Flow

**Section:** 006 — Running the End-to-End GPU Pipeline
**Lecture#:** 000
**Sheet title:** From S3 Input to GPU Job: Following the Execution Flow
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 006-000-from-s3-input-to-gpu-job--foll

---

The infrastructure is ready. Now we will follow one vendor folder from S3 to a finished catalog row. Keep the sequence clear, because each hop has a different failure symptom.

Start with the input. Photos are already under `images/<stem>/` in the images bucket. That prefix is the unit of work. Your laptop, or an earlier pipeline step, uploads or syncs those objects. Batch captions what exists under the prefix; it does not create the input.

Next, submit to `gpu-teaching-gpu-smoke-queue-spot` and name `gpu-teaching-caption-job`. The submission points the container at the stem by passing the bucket names, `IMAGE_PREFIX`, `BATCH_SIZE`, and the command `python /app/describe_items.py`. Batch accepts the request and looks for capacity in the compute environment behind the queue.

When the instance is ready and the container starts, `gpu-teaching-batch-job-role` lets the process list and download objects under the prefix. BLIP runs on the GPU, and the process writes `descriptions/<stem>/descriptions.csv` to the catalog bucket. Container logs go to `/aws/batch/job`. Your laptop polls the Batch status; it does not need a shell inside the container.

The pattern is durable input, asynchronous compute, and structured output. This lab keeps it to one folder and one CSV so every hop remains visible. The wider industry reference remains in Further reading.

Before we run it, predict the first check for each symptom: an empty catalog, a job waiting in `RUNNABLE`, or a container failing after startup. Then use the sequence: verify S3 input, submit with overrides, wait for GPU placement, inspect the container logs, and read the CSV.

Next, we slow down on the status field, from `SUBMITTED` through `SUCCEEDED`, and map each state to the checks it supports.

---

## Further reading (not spoken)

- [AWS Batch: Submitting a job](https://docs.aws.amazon.com/batch/latest/userguide/SubmitJob.html) — submit API and parameters
- [Amazon S3: Organizing objects with prefixes](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-prefixes.html) — prefix as the work unit
- [DoorDash Engineering Blog](https://doordash.engineering/blog/) — marketplace catalog and data pipeline context
