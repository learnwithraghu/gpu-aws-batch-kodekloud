# Video 09 — Demo: logs via describe-jobs
**Type:** Demo
**Runtime target:** ~3 minutes

---

Next up. Same job id, but now we read the logs. I want the ops loop, not a new submit. Job id, then metadata, then the log stream, then one line I can act on. The id is the one the previous clip stored in JOB_ID.

Same terminal, region ap-northeast-1, env file sourced. I run aws batch describe-jobs on JOB_ID. The query pulls status, statusReason, exit code, and logStreamName. If the job has not started, log comes back empty. That is normal for RUNNABLE.

When there is a stream name, I run aws logs get-log-events. Log group /aws/batch/job. Stream name from describe-jobs. Region ap-northeast-1. Messages exist only after STARTING or RUNNING. Job definition is still gpu-teaching-caption-job, highest active revision, with explicit awslogs to this group. Revision one and two are not what I submitted.

On a healthy SUCCEEDED job, exit code is zero and the stream is present. Lines in order: Device cuda. Loading caption model. Model ready, Listing photos. Found, a count. Then one line per photo: key, arrow, caption, accepted or rejected in brackets. Then Wrote with row count and accepted and rejected totals to descriptions/sample/descriptions.csv. Columns are image_s3_uri, item_description, photo_status. I read the count off that Wrote line. Lesson nine checks the object.

If FAILED with exit code one, I trust the line, not the badge. AccessDenied means job role or bucket policy. Device cpu or CUDA false means AMI or GPU placement. ModuleNotFoundError means the ECR image does not match the program. Found 0 images means IMAGE_PREFIX or the upload path. Out of memory often means too many photos at once. BATCH_SIZE was eight. Fix the lowest layer first.

If still RUNNABLE, I stop. Often no log stream. Stuck RUNNABLE is Spot capacity or the on-demand G and VT quota, not a Python bug. I do not edit describe_items.py from an empty log group.

Batch orchestrated the run. The CSV is the product. Next lesson reads it the way KodeFood would.
