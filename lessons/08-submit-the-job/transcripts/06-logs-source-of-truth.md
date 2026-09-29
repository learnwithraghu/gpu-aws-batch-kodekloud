# Video 06 — Logs as source of truth
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

Container logs are the standard output and standard error of the process, shipped to CloudWatch Logs. In this course the log group is /aws/batch/job. There is one log stream per job attempt. The job record can carry logStreamName, which is the direct name of that stream.

Status alone is a headline. FAILED with exit code one only says something exited non-zero. The line in the stream says which layer broke. AccessDenied, often on GetObject, means the job role or the bucket policy. The role in this course is the one on gpu-teaching-caption-job, and an empty job role ARN fails the first S3 call even after the GPU starts. A CUDA problem shows up in two places. The default command in the definition prints whether torch.cuda.is_available is true or false. The catalog program prints Device, then cuda or cpu. False, or Device cpu, points at the AMI or at GPU placement, not at the prompt. ModuleNotFoundError means the image drifted from the code you think you ran. An empty photo list prints Found 0 images, then exits with No images to describe. That is IMAGE_PREFIX or the upload path, not the model. An out of memory kill comes from the kernel, often because too many photos were handed to the T4 at once. BATCH_SIZE eight is the course setting for that reason.

The workflow is short. Run describe-jobs on the job id. Copy logStreamName from the attempt. Open CloudWatch on /aws/batch/job, or call get-log-events with that stream name, in ap-northeast-1. Fix the lowest layer first. Network, then IAM, then CUDA, then the model. Do not retune BLIP because the role cannot read a photo.

Two limits keep this honest. There is no stream while the job is still RUNNABLE. The container has not started, so prints inside describe_items.py cannot appear. And the stream exists when the container runs only if the job definition sends logs with the awslogs driver to /aws/batch/job. That explicit log configuration is on the revisions you should actually run. Submit the name gpu-teaching-caption-job and let Batch pick the highest active revision. Do not submit revision one or revision two. Revision one asks for too much memory and never places. Revision two has no job role. Revision three has the job role and still has no explicit log configuration. Later revisions set the awslogs driver, the group, the region, and a stream prefix. The describe-jobs query this course uses returns status, statusReason, the exit code, and logStreamName from the first attempt, so you can paste the stream into get-log-events without hunting the console. You can also open a live tail on that stream in CloudWatch once STARTING has created it. The group is /aws/batch/job either way.

On the screen, a FAILED badge sits next to a magnifying glass on one log line, and three labels sit under it, IAM, prefix, and CUDA.

Cancel and resubmit, so you do not leave two jobs writing one CSV, is next.
