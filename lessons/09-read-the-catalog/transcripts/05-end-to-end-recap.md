# Video 05 — End-to-end recap
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

You can now walk a real GPU batch path, and the path is one chain. Photos land in S3. A Python program splits the work, I/O in one file and the GPU in another. A container image is built for amd64 with pinned dependencies. That image is pushed to ECR so an instance can pull it. Batch supplies a GPU compute environment, a queue, a job definition, and roles. A submit adds overrides. Logs explain failures. A CSV comes out. The app reads the CSV.

The same chain, as the lessons actually taught it, has six stations. Data is the S3 prefixes for photos and for the CSV. Program is the container code, listing and writing on one side, the model on the other. Image is the amd64 build. Registry is the ECR push. Scheduler is the compute environment, the queue, the job definition, and the split between instance permissions and the job role. Run is submit, wait, and the status and log diagnosis.

The live names on that last station are the ones you reuse for the next vendor folder. Region ap-northeast-1. Queue gpu-teaching-gpu-smoke-queue-spot. The on-demand queue is gpu-teaching-gpu-smoke-queue-on-demand, and you use it only after the on-demand G and VT quota, L-DB2E81BA, is at least four. Job definition gpu-teaching-caption-job, submitted by name so Batch picks the highest active revision. You do not submit revision one or revision two. Memory is twelve thousand two hundred eighty-eight mebibytes. GPU count is one. The command override is python /app/describe_items.py. The environment carries IMAGE_PREFIX, such as images/sample, the two bucket variables, and BATCH_SIZE. The CSV lands at descriptions, then the stem, then descriptions.csv, with columns image_s3_uri and item_description. Logs are in /aws/batch/job, and they appear only after STARTING or RUNNING, not while the job sits in RUNNABLE. A stuck RUNNABLE is Spot capacity or that on-demand quota, not a Python bug.

The checklist for the next folder is short. Sync the photos to images, then the stem. Submit with a matching IMAGE_PREFIX, and match the job name to that stem. Wait until SUCCEEDED. Read descriptions, then the same stem, then descriptions.csv, and compare the data rows to the jpg, jpeg, and png keys. Rebuild only when the container program or the Dockerfile changed. A new photo does not need a new image. A new prompt does.

What you can do with that checklist is design an offline GPU batch that scales back toward zero when the queue is idle, tell a RUNNABLE wait from a container failure, keep the job role separate from the instance role, and treat the CSV as the product. The scheduler is not the menu. The compute environment minimum is zero vCPUs, so a GPU does not stay up while the class is idle. The CSV does not disappear when that count goes back to zero.

On the screen, the six stations sit in a loop, photos, program, image, registry, scheduler, and run, and the loop closes on the CSV the app reads.

The last clip prints that file and counts the rows.
