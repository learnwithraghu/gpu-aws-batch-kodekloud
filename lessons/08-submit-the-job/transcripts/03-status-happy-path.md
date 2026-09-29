# Video 03 — Status happy path
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

A job status is the string Batch updates as its control plane and the container agent move the work forward. It is the first screen in operations. You read it before CloudWatch, and you read it before you look in S3.

Each state exists for a different handoff. SUBMITTED means the record was created and validation passed. RUNNABLE means the job is eligible to run and is waiting for the scheduler to place it, or waiting for capacity. STARTING means an instance was selected and the agent is pulling the image, creating the container, and launching the task. RUNNING means your process is executing, which in this course is describe_items.py. SUCCEEDED and FAILED both mean the container has exited and Batch recorded an exit code. SUCCEEDED is exit code zero. FAILED is the process or the infrastructure giving up.

The happy path in this course is SUBMITTED, then RUNNABLE, then STARTING, then RUNNING, then SUCCEEDED. Picture the Spot queue gpu-teaching-gpu-smoke-queue-spot in ap-northeast-1. The compute environment scales from zero. STARTING pulls the gpu-teaching image, tag latest, from ECR. RUNNING is the catalog program. A healthy log, once the stream exists, shows Device and then cuda, then Loading caption model, and a note that the first run may download weights. Then Model ready, Listing photos. Then Found, and a count of images under the prefix. Then one line per photo. Then Wrote, and a count, to descriptions, then the folder stem, then descriptions.csv. For IMAGE_PREFIX images/sample, that object is descriptions/sample/descriptions.csv, with columns image_s3_uri and item_description.

SUCCEEDED only means the container exited zero. The process believed it finished. It does not, by itself, prove the CSV schema is right, or that the key is the one the app will read. If the program listed the wrong prefix, or wrote nothing the app can see, the scheduler can still say SUCCEEDED. Lesson nine checks the object. Correct key, row count, and those two column names.

During RUNNABLE the log group /aws/batch/job has no stream for this attempt. Quiet logs in that state are the wait, not a failed model. The stream can appear at STARTING. The first RUNNING can also take several minutes while the weights download, and that can still be this same happy path. Without the command override, a zero exit would only mean the CUDA check printed true or false. With the override, RUNNING means describe_items.py.

The job definition you submit by name is gpu-teaching-caption-job, so Batch uses the highest active revision. That revision should ask for one GPU and twelve thousand two hundred eighty-eight mebibytes. The command override is python /app/describe_items.py, with IMAGE_PREFIX, the two bucket variables, and BATCH_SIZE. Status tells you whether that process got a machine. It does not open the CSV.

On the screen, a state machine shows the green path SUBMITTED, RUNNABLE, STARTING, RUNNING, SUCCEEDED, with FAILED as the other exit. A note beside SUCCEEDED says to still check the CSV.

A long RUNNABLE with no logs is the diagnosis next.
