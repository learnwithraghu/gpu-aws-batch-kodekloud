# Video 06 — Logs as source of truth
**Type:** Theory
**Runtime target:** ~3 minutes

---

Alright. When the GPU did something, the log is the truth. Container logs are stdout and stderr shipped to CloudWatch. In this course the log group is /aws/batch/job. One stream per attempt. The job record can carry logStreamName.

Status alone is a headline. FAILED with exit code one only says something exited non-zero. The line says which layer broke. AccessDenied on GetObject means the job role or bucket policy. Empty jobRoleArn fails the first S3 call even after the GPU starts. CUDA shows up two ways. The default command prints torch.cuda.is_available. The catalog program prints Device cuda or cpu. False or Device cpu points at the AMI or GPU placement, not the prompt. ModuleNotFoundError means the image drifted. Found 0 images then No images to describe means IMAGE_PREFIX or the upload path. Out of memory often means too many photos on the T4 at once. BATCH_SIZE eight is the course setting for that reason.

On a healthy run you also see the product shape. Each photo prints as key, arrow, caption, and accepted or rejected in brackets. The line after the write reports row count with accepted and rejected totals from photos.save_csv. Those lines are how you know KodeFood gets a three-column CSV, not only that the process exited zero.

Workflow: describe-jobs on the job id, copy logStreamName, then get-log-events on /aws/batch/job in the same region as the job. Fix the lowest layer first. Network, then IAM, then CUDA, then the model. Do not retune BLIP because the role cannot read a photo.

No stream while RUNNABLE. And the stream exists only if the job definition sends awslogs to /aws/batch/job. Submit the definition by name for the highest active revision from lesson 07—that revision must have the job role and awslogs. Broken revisions never place or lack S3 and logs. The course describe-jobs query returns status, statusReason, exit code, and logStreamName so you can paste the stream without hunting.

Cancel and resubmit, so two jobs do not write one CSV, is next.
