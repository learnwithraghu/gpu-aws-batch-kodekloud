# Lesson 08 — Submit the job

One CLI submission runs one folder. The image is in ECR, the photos are in `images/sample/`, and the queue and job definition exist from lesson 07.

```bash
set -a && source .env && set +a
export AWS_DEFAULT_REGION=ap-northeast-1
```

`BATCH_JOB_QUEUE` should be `gpu-teaching-gpu-smoke-queue-spot`. `BATCH_JOB_DEFINITION` should be `gpu-teaching-caption-job`.

## Submit

The override replaces the CUDA-check command with the catalog program and tells it which folder to read. `BATCH_SIZE` is how many photos the GPU holds at once.

```bash
JOB_ID=$(aws batch submit-job \
  --region "$AWS_DEFAULT_REGION" \
  --job-name describe-items-sample \
  --job-queue "$BATCH_JOB_QUEUE" \
  --job-definition "$BATCH_JOB_DEFINITION" \
  --container-overrides "{
    \"command\": [\"python\", \"/app/describe_items.py\"],
    \"environment\": [
      {\"name\": \"S3_BUCKET\", \"value\": \"${S3_BUCKET}\"},
      {\"name\": \"S3_CSV_BUCKET\", \"value\": \"${S3_CSV_BUCKET}\"},
      {\"name\": \"IMAGE_PREFIX\", \"value\": \"images/sample\"},
      {\"name\": \"BATCH_SIZE\", \"value\": \"8\"}
    ]
  }" \
  --query jobId --output text)

echo "$JOB_ID"
```

Change `images/sample` and the job name together if the folder stem is not `sample`.

## Wait

```bash
while true; do
  STATUS=$(aws batch describe-jobs --jobs "$JOB_ID" \
    --query 'jobs[0].status' --output text)
  echo "$STATUS"
  case "$STATUS" in SUCCEEDED|FAILED) break ;; esac
  sleep 15
done
```

The path is `SUBMITTED` → `RUNNABLE` → `STARTING` → `RUNNING` → `SUCCEEDED`.

The first run on a new instance also downloads the BLIP weights, so `RUNNING` can last several minutes. A job that stays in `RUNNABLE` is usually Spot. Point `.env` at the on-demand queue and submit again:

```bash
BATCH_JOB_QUEUE=gpu-teaching-gpu-smoke-queue-on-demand
```

Cancel the stuck job before you resubmit, or you will pay for two runs if Spot appears later:

```bash
aws batch cancel-job --job-id "$JOB_ID" --reason "no Spot capacity, resubmitting on-demand"
```

## If it fails

```bash
aws batch describe-jobs --jobs "$JOB_ID" \
  --query 'jobs[0].{status:status,reason:statusReason,exit:attempts[0].container.exitCode,log:attempts[0].container.logStreamName}'
```

Then read the container log. The stream name is in that output:

```bash
aws logs get-log-events \
  --log-group-name /aws/batch/job \
  --log-stream-name '<log stream from describe-jobs>' \
  --region "$AWS_DEFAULT_REGION" \
  --query 'events[].message' --output text
```

On `SUCCEEDED`, the CSV is at `s3://$S3_CSV_BUCKET/descriptions/sample/descriptions.csv`. Lesson 09 prints it.
