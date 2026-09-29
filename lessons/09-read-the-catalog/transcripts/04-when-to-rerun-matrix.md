# Video 04 — When to re-run what
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

A change in this system hits three different places, and they are not the same button. You might rebuild the image. You might upload photos again. You might resubmit the Batch job. Most wasted GPU time comes from doing all three when only one of them changed.

New photos in the same folder do not need a new image. You sync the objects under images, then the stem, which for the sample is images/sample. Then you resubmit. The job definition name stays gpu-teaching-caption-job, so Batch picks the highest active revision. You do not submit revision one or revision two. The override command stays python /app/describe_items.py. IMAGE_PREFIX stays on that same folder. S3_BUCKET and S3_CSV_BUCKET stay the bucket variables. BATCH_SIZE stays eight. The queue stays gpu-teaching-gpu-smoke-queue-spot in ap-northeast-1, unless you have already confirmed the on-demand quota and you mean to use the on-demand queue. The definition still asks for one GPU and twelve thousand two hundred eighty-eight mebibytes.

A better prompt, a generate setting, or a code change does need a new image. That is the build and the ECR push from lessons three and four. You do not re-upload the photos if the bytes in S3 were already right. You do resubmit, because Batch runs the image that was baked, not the file on your laptop. Until that push exists, another submit repeats the old program.

A FAILED job after a fix follows the thing you fixed. Rebuild only if the code or the image changed. Re-upload only if the data was wrong. Always resubmit. Read the log in /aws/batch/job first, and only after the job has reached STARTING or RUNNING. AccessDenied is the role. An empty list is the prefix. A CUDA false result is the AMI or the GPU placement. If the job never left RUNNABLE, you do not rebuild. Stuck RUNNABLE is Spot capacity or the on-demand G and VT quota, code L-DB2E81BA. Cancel the stale attempt before the new submit so two jobs do not race on one key.

If you only want to read the catalog again, you rebuild nothing, you upload nothing, and you submit nothing. The object is already at descriptions, then the stem, then descriptions.csv. Re-reading is an S3 copy, which is the last clip in this lesson.

Sync from lesson six copies the folder. It does not submit the job. Submit is a separate call, and you cancel any stuck attempt first so two writers do not share the key.

Re-running a successful folder overwrites that same key. That is intentional. The latest successful catalog for the stem wins. Operators always know the path. This course keeps one active attempt per folder so the overwrite is a sequence, not a race.

On the screen, a table has four rows. New photos, same folder. Prompt or code. FAILED after a fix. Read the existing catalog. Each row has three answers, rebuild, re-upload, and resubmit.

The full path, from photos to the app, is the recap next.
