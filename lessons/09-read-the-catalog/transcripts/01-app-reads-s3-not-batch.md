# Video 01 — The app reads S3, not Batch
**Type:** Theory
**Runtime target:** ~3 minutes

---

Hello. Welcome to the last lesson. KodeFood consumes an object in S3. The object is descriptions, then the folder stem, then descriptions.csv, in the CSV bucket. For sample that key is descriptions/sample/descriptions.csv. The app does not call SubmitJob. It does not poll RUNNABLE, STARTING, or SUCCEEDED. Batch is the offline worker. The product is the file.

That split matters because a mobile or web app should not need permission to submit GPU jobs, and it should not loop on a scheduler. It needs a stable artifact. Downstream services depend on the artifact contract, not the Batch API. The file is one header plus one row per photo. The header is image_s3_uri, item_description, and photo_status. Rejected rows stay in the file. The app uses the accepted rows for the menu. If the CSV is missing, the app is broken, even when yesterday's job succeeded on a different stem.

Here is the course failure. A job on gpu-teaching-gpu-smoke-queue-spot in ap-northeast-1 reaches SUCCEEDED. IMAGE_PREFIX was images/wrong-stem, so the write landed at descriptions/wrong-stem/descriptions.csv. The app still reads descriptions/sample/descriptions.csv. The menu is empty. The Batch console is green. Scheduler success and product success came apart. The app never learns the columns from the job id.

The worker path is familiar. Photos under an images prefix. Submit gpu-teaching-caption-job by name for the highest active revision. Override command python /app/describe_items.py. Environment carries buckets, IMAGE_PREFIX, and BATCH_SIZE. Definition asks for one GPU and twelve thousand two hundred eighty-eight mebibytes. Logs in /aws/batch/job appear only after STARTING or RUNNING. None of that is what the app calls. When the container exits zero, the app's next read is the CSV key for that stem.

A missing file and a wrong stem look the same from the app. Both are an empty catalog. Stuck RUNNABLE never writes at all. That wait is Spot capacity or the on-demand G and VT quota, not a menu bug. Polling the job id would couple KodeFood to Spot capacity. Wrong dependency. The job id from lesson eight never belongs in the app.

The three column names are the contract. That is next.
