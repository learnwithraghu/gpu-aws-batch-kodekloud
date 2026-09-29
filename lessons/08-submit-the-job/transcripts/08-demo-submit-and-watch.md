# Video 08 — Demo: submit and watch
**Type:** Demo
**Runtime target:** ~3 minutes

---

Okay. Time to submit for real. I want one job id that ties the job definition, the Spot queue, and this folder's overrides. Then I want status and statusReason until the job succeeds or fails for a reason I can act on. Image is in ECR. Photos are under images/sample. Queue and job definition already exist. This clip is the submit.

I am in the terminal. Region ap-northeast-1. I load the env file with set -a, source .env, set +a, and export AWS_DEFAULT_REGION.

BATCH_JOB_QUEUE should be gpu-teaching-gpu-smoke-queue-spot. I am not using the on-demand fallback. BATCH_JOB_DEFINITION should be gpu-teaching-caption-job. I pass that name only so Batch picks the highest active revision. Do not submit revision one or two. That revision should ask for one GPU and twelve thousand two hundred eighty-eight mebibytes.

I run aws batch submit-job. Job name describe-items-sample. Queue and definition from those variables. Container overrides set command to python /app/describe_items.py. Environment sets S3_BUCKET, S3_CSV_BUCKET, IMAGE_PREFIX images/sample, BATCH_SIZE 8. I store the job id in JOB_ID and echo it. If the stem were not sample, I would change images/sample and the job name together.

I run bash helpers/watch_batch_job.sh with that job id.

A healthy watch polls every fifteen seconds in ap-northeast-1 and reminds you that CloudWatch logs appear only after STARTING or RUNNING. Each poll prints time, status, statusReason, exit code, and log stream when present. Healthy order: SUBMITTED, RUNNABLE, STARTING, RUNNING, SUCCEEDED. When STARTING or RUNNING, the helper names /aws/batch/job and the stream. First RUNNING on a new instance can last several minutes while BLIP weights download. SUCCEEDED means exit zero. The product is descriptions/sample/descriptions.csv with accepted and rejected rows. The next lesson prints it.

If the job stays RUNNABLE, I do not open Python. After about two minutes the helper says no container has started. It prints desired vCPUs and the GPU quota. On Spot that code is L-3819A6DF. Long RUNNABLE here is usually Spot capacity. I do not flip to on-demand because Spot is quiet. L-DB2E81BA is often zero, and then that queue never starts a container either.

The next clip takes this job id into describe-jobs and opens the log stream.
