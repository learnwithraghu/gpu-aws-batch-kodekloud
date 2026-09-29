# Video 09 — Demo: logs via describe-jobs
**Type:** Demo
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

I want the ops loop, not a new submit. Job id, then the job metadata, then the log stream, then one line I can act on. The id is the one the previous clip stored in JOB_ID. If the watch already printed a status, this query should show that same status.

I am in the same terminal, region ap-northeast-1, with the env file already sourced. I run aws batch describe-jobs. The jobs flag is JOB_ID. The query pulls four fields from the first job. Status. statusReason, which I label reason. The exit code on attempts zero, container. And logStreamName on that same container, which I label log. If the job has not started, that log field comes back empty. That is normal for RUNNABLE. It is not a broken log group.

When the query shows a stream name, I run aws logs get-log-events. The log group name is /aws/batch/job. The log stream name is the value from describe-jobs, not a name I guess. The region is AWS_DEFAULT_REGION, ap-northeast-1. The query is the message on each event, printed as text. Those messages exist only after the job has reached STARTING or RUNNING. The job definition name is still gpu-teaching-caption-job, highest active revision, with explicit awslogs to this group. Revision one and revision two are not what I submitted.

On a healthy SUCCEEDED job the status is SUCCEEDED and the exit code is zero. The stream is present. The lines I look for, in order, are Device and then cuda. Then Loading caption model, including the note that the first run may download weights. Then Model ready, Listing photos. Then Found, a count, images in the images bucket under the prefix. Then one line per photo, the key and the sentence. Then Wrote, a count of descriptions, to the CSV bucket at descriptions/sample/descriptions.csv. That file has the columns image_s3_uri and item_description. I do not read a row count off the status. I read it off that Wrote line, and lesson nine checks the object.

If the status is FAILED, exit code one, I use the same two commands and I trust the line, not the badge. AccessDenied on GetObject means the job role or the bucket policy. Device cpu, or the CUDA check printing false, means the AMI or GPU placement. ModuleNotFoundError means the image in ECR does not match the program I think I built. Found 0 images, then No images to describe, means IMAGE_PREFIX or the upload path. An out of memory kill means the process died in the kernel, often from handing the GPU too much at once. BATCH_SIZE on this submit was eight. I fix the lowest layer first.

If the job is still RUNNABLE, I stop. There is often no log stream. Stuck RUNNABLE is Spot capacity, or the on-demand G and VT quota, not a Python bug. I do not edit describe_items.py from an empty log group.

Batch orchestrated the run. The CSV is the product. The next lesson reads descriptions/sample/descriptions.csv the way the food app would.
