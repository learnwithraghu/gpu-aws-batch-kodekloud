# Video 04 — When to re-run what
**Type:** Theory
**Runtime target:** ~3 minutes

---

So, when something changes, which button do you press? A change hits three different places, and they are not the same button. You might rebuild the image. You might upload photos again. You might resubmit the Batch job. Most wasted GPU time comes from doing all three when only one changed.

New photos in the same folder do not need a new image. Sync under images, then the stem, for sample images/sample. Then resubmit. Job definition stays gpu-teaching-caption-job by name. Override stays python /app/describe_items.py. IMAGE_PREFIX stays on that folder. Buckets and BATCH_SIZE eight stay. Queue stays gpu-teaching-gpu-smoke-queue-spot in ap-northeast-1 unless you have confirmed on-demand quota and mean to switch. Definition still asks for one GPU and twelve thousand two hundred eighty-eight mebibytes. The new CSV again carries image_s3_uri, item_description, and photo_status for every photo, accepted and rejected.

A better prompt, generate setting, or code change needs a new image. Build and ECR push from lessons three and four. Do not re-upload photos if the bytes were already right. Do resubmit, because Batch runs the baked image, not the file on your laptop. A change to how accepted and rejected are marked is a code change. Rebuild and push before the next job.

A FAILED job after a fix follows what you fixed. Rebuild only if code or image changed. Re-upload only if data was wrong. Always resubmit. Read /aws/batch/job first, only after STARTING or RUNNING. AccessDenied is the role. Empty list is the prefix. CUDA false is the AMI or GPU placement. If the job never left RUNNABLE, do not rebuild. Stuck RUNNABLE is Spot capacity or on-demand quota L-DB2E81BA. Cancel the stale attempt before the new submit so two jobs do not race on one key.

If you only want to read the catalog again, rebuild nothing, upload nothing, submit nothing. The object is already at descriptions, stem, descriptions.csv. Re-reading is an S3 copy, the last clip in this lesson.

Re-running a successful folder overwrites that same key. Intentional. Latest successful catalog for the stem wins. One active attempt per KodeFood vendor folder so the overwrite is a sequence, not a race.

The full path from photos to the app is the recap next.
