# Video 08 — Demo: submit and watch
**Type:** Demo
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

I want one job id that ties the job definition, the Spot queue, and this folder's overrides together. Then I want the status, including statusReason, until the job succeeds or fails for a reason I can act on. The image is already in ECR. The photos are already under images/sample. The queue and the job definition already exist. This clip is the submit, not the setup.

I am in the terminal. The region is ap-northeast-1. I load the env file with set -a, then source .env, then set +a, so the bucket names, the queue, and the job definition are in the shell. I export AWS_DEFAULT_REGION to ap-northeast-1.

I check two variables before I submit. BATCH_JOB_QUEUE should be gpu-teaching-gpu-smoke-queue-spot. I am not using the fallback queue, gpu-teaching-gpu-smoke-queue-on-demand. BATCH_JOB_DEFINITION should be gpu-teaching-caption-job. I will pass that name only, so Batch picks the highest active revision. I do not submit revision one or revision two. The revision Batch picks should ask for one GPU and twelve thousand two hundred eighty-eight mebibytes.

I run aws batch submit-job. The region flag is the default region. The job name is describe-items-sample. The job queue is BATCH_JOB_QUEUE. The job definition is BATCH_JOB_DEFINITION. Container overrides set the command to python, then /app/describe_items.py. That replaces the CUDA check. The environment sets S3_BUCKET and S3_CSV_BUCKET from the shell, IMAGE_PREFIX to images/sample, and BATCH_SIZE to 8. Eight is how many photos the GPU holds at once. I ask for the job id as text and store it in JOB_ID. Then I echo JOB_ID. Whatever that echo prints is the id I pass to the watch command. If the folder stem were not sample, I would change images/sample and the job name together.

I run bash helpers/watch_batch_job.sh and pass that job id.

A healthy watch starts by saying it is watching the job in ap-northeast-1, every fifteen seconds, and that CloudWatch logs appear only after STARTING or RUNNING, not while the job sits in RUNNABLE. Each poll prints the time, the status, statusReason when Batch has one, the exit code when there is one, and the log stream name when there is one. The healthy order is SUBMITTED, then RUNNABLE, then STARTING, then RUNNING, then SUCCEEDED. I am not claiming how many seconds each state will last. When the status becomes STARTING or RUNNING, the helper names the log group /aws/batch/job and the stream, once Batch provides it. The first RUNNING on a new instance can last several minutes while the BLIP weights download. SUCCEEDED means the container exited zero. The product is descriptions/sample/descriptions.csv in the CSV bucket. The next lesson prints it.

If the job stays RUNNABLE, I do not open Python. After about two minutes the helper says no container has started, so this is not describe_items.py. It prints the queue, the compute environment's desired vCPU count, and the GPU quota. On this Spot queue that code is L-3819A6DF. A long RUNNABLE here is usually Spot capacity. I do not flip to on-demand because Spot is quiet. The on-demand quota L-DB2E81BA is often zero, and then that queue never starts a container either.

The next clip takes this same job id into describe-jobs and opens the log stream.
