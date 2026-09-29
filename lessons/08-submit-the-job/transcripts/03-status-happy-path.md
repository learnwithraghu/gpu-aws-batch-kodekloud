# Video 03 — Status happy path
**Type:** Theory
**Runtime target:** ~3 minutes

---

So, a job status is the string Batch updates as work moves forward. Read it before CloudWatch, and before you look in S3.

SUBMITTED means the record was created and validation passed. RUNNABLE means eligible and waiting for placement or capacity. STARTING means an instance was selected and the agent is pulling the image and creating the container. RUNNING means your process is executing, here describe_items.py. SUCCEEDED is exit code zero. FAILED is the process or infrastructure giving up.

Happy path: SUBMITTED, RUNNABLE, STARTING, RUNNING, SUCCEEDED. Your Spot queue from lesson 07 drives that path. The compute environment scales from zero. STARTING pulls the image tag from ECR. RUNNING is the catalog program. A healthy log shows Device cuda, Loading caption model, Model ready, Listing photos, Found and a count. Then one line per photo: key, arrow, caption, and accepted or rejected in brackets. Then Wrote with row count and accepted and rejected totals to descriptions, stem, descriptions.csv. For images/sample that object is descriptions/sample/descriptions.csv, columns image_s3_uri, item_description, photo_status.

SUCCEEDED only means the container exited zero. It does not prove the CSV schema is right, or that the key is the one KodeFood will read. Wrong prefix and the scheduler can still say SUCCEEDED. Lesson nine checks the object: key, row count, three column names.

During RUNNABLE, /aws/batch/job has no stream for this attempt. Quiet logs are the wait, not a failed model. The stream can appear at STARTING. First RUNNING can take several minutes while weights download and still be this happy path.

Submit the job definition by name so Batch uses the highest active revision from lesson 07, with the GPU and memory that revision asks for. Override command python /app/describe_items.py, with IMAGE_PREFIX, buckets, and BATCH_SIZE. Status tells you whether that process got a machine. It does not open the CSV.

A long RUNNABLE with no logs is next.
