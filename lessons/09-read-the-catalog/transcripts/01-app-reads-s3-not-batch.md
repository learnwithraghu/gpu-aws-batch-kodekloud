# Video 01 — The app reads S3, not Batch
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

The food app consumes an object in S3. The object is descriptions, then the folder stem, then descriptions.csv, in the CSV bucket. For the sample folder that key is descriptions/sample/descriptions.csv. The app does not call SubmitJob. It does not poll RUNNABLE, STARTING, or SUCCEEDED. Batch is the offline worker. The product is the file.

That split matters because a mobile app or a web app should not need permission to submit GPU jobs, and it should not sit in a loop on a scheduler. It needs a stable artifact. Same idea as reading a nightly export from a warehouse, rather than logging into the query engine that produced the export. Downstream services depend on the artifact contract, not on the Batch API. The file is one header plus one row per photo. The header is image_s3_uri and item_description. A copy exported somewhere else is still that same contract. If the CSV is missing, the app is broken, even when yesterday's job succeeded on a different stem.

Here is the course failure. A job on gpu-teaching-gpu-smoke-queue-spot, in ap-northeast-1, reaches SUCCEEDED. Its IMAGE_PREFIX was images/wrong-stem, so the write landed at descriptions/wrong-stem/descriptions.csv. The app still reads descriptions/sample/descriptions.csv. The menu is empty. The Batch console is green. Scheduler success and product success came apart. The columns on the real file are image_s3_uri and item_description. The app never learns that from the job id.

The worker side is the path from the earlier lessons. Photos live under an images prefix in the images bucket. The submit uses the job definition name gpu-teaching-caption-job, so Batch picks the highest active revision, not revision one or revision two. The override command is python /app/describe_items.py. The environment carries the two bucket variables, IMAGE_PREFIX, and BATCH_SIZE. The definition asks for one GPU and twelve thousand two hundred eighty-eight mebibytes. Logs in /aws/batch/job appear only after STARTING or RUNNING. None of that machinery is what the app calls. When the container exits zero, the app's next read is the CSV key for that stem.

A missing file and a wrong stem look the same from the app. Both are an empty catalog. Stuck RUNNABLE never writes the file at all, and that wait is Spot capacity or the on-demand G and VT quota, not a bug in the menu code. The app cannot tell those apart by calling Batch, because the app does not call Batch.

On the screen, one arrow runs from Batch to S3, and a separate arrow runs from the app straight to the same bucket. There is no arrow from the app back to the queue. The worker can be SUBMITTED, RUNNABLE, or FAILED, and the menu does not change until that object changes. Polling the job id would couple the food app to Spot capacity. That is the wrong dependency. The job id from lesson eight never belongs in the app.

The CSV is a small interface, and the column names are the contract. That is next.
