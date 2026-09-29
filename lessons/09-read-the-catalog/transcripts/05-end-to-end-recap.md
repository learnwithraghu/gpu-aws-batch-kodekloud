# Video 05 — End-to-end recap
**Type:** Theory
**Runtime target:** ~3 minutes

---

Okay. Let's put the whole path in one pass. You can now walk a real GPU batch path. Photos land in S3. A Python program splits I/O and GPU work. A container image is built for amd64 with pinned dependencies. That image is pushed to ECR. Batch supplies a GPU compute environment, a queue, a job definition, and roles. A submit adds overrides. Logs explain failures. A CSV comes out. KodeFood reads the CSV.

Six stations as the lessons taught them. Data is the S3 prefixes for photos and CSV. Program is the container code. Image is the amd64 build. Registry is the ECR push. Scheduler is the compute environment, queue, job definition, and the split between instance permissions and the job role. Run is submit, wait, and status and log diagnosis.

Live names for the next vendor folder. Region ap-northeast-1. Queue gpu-teaching-gpu-smoke-queue-spot. On-demand queue gpu-teaching-gpu-smoke-queue-on-demand only after L-DB2E81BA is at least four. Job definition gpu-teaching-caption-job by name, highest active revision. Do not submit revision one or two. Memory twelve thousand two hundred eighty-eight mebibytes. GPU one. Override command python /app/describe_items.py. Environment carries IMAGE_PREFIX such as images/sample, the buckets, and BATCH_SIZE. CSV lands at descriptions, stem, descriptions.csv with columns image_s3_uri, item_description, and photo_status. Rejected rows stay. The app uses accepted rows. Logs in /aws/batch/job appear only after STARTING or RUNNING. Stuck RUNNABLE is Spot capacity or that on-demand quota, not a Python bug.

Checklist for the next folder. Sync photos to images, stem. Submit with matching IMAGE_PREFIX and job name. Wait until SUCCEEDED. Read descriptions, same stem, descriptions.csv, and compare data rows to jpg, jpeg, and png keys. Rebuild only when the container program or Dockerfile changed. A new photo does not need a new image. A new prompt does.

What that checklist buys you. An offline GPU batch that scales toward zero when idle. A way to tell RUNNABLE wait from a container failure. Job role separate from instance role. CSV as the product. The scheduler is not the menu. Min vCPUs zero, so a GPU does not stay up while the class is idle. The CSV stays when that count goes back to zero.

The last clip prints that file and counts the rows.
