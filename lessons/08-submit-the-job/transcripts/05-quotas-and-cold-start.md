# Video 05 — Quotas and cold start
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

A service quota is a hard account limit on a class of resources. Here the class is EC2 G and VT capacity, the family that includes g4dn. A compute environment whose status is VALID does not override that limit. Batch can only start a g4dn.xlarge if the account is allowed to buy that purchase option. get-service-quota is the ground truth.

Two codes match the two queues, both in ap-northeast-1. The Spot queue is gpu-teaching-gpu-smoke-queue-spot. Its quota is L-3819A6DF, All G and VT Spot Instance Requests. You need at least four, and this course often has eight. The on-demand queue is gpu-teaching-gpu-smoke-queue-on-demand. Its quota is L-DB2E81BA, Running On-Demand G and VT instances. You need at least four before one g4dn.xlarge can run there. A value of zero is common on a new account. Then the on-demand queue never starts a container, the job stays RUNNABLE, and /aws/batch/job stays empty. That is not a Python bug.

You check the on-demand code with aws service-quotas get-service-quota, service code ec2, quota code L-DB2E81BA, region ap-northeast-1. The same call with L-3819A6DF checks Spot. The watch helper picks the code from the compute environment type. A Spot environment prints L-3819A6DF. Any other type prints L-DB2E81BA. A printed value of zero means no g4dn will start, and /aws/batch/job stays empty. A non-zero Spot quota plus a long RUNNABLE is usually capacity in this availability zone. If L-DB2E81BA is zero, you request an increase in the console under Service Quotas, Amazon EC2, that quota, Request increase. Or you run request-service-quota-increase for the same code, desired value eight, same region. Approval can take hours or days. Until get-service-quota shows at least four, keep BATCH_JOB_QUEUE on the Spot queue. Do not treat on-demand as an automatic escape hatch.

Cold start is a different slowness, and it only begins after placement. The first job on a fresh instance, or the first job after a long idle, does three slow things. The instance boots. The agent pulls a multi-gigabyte image from ECR. The container downloads the BLIP weights on first use. The program prints Loading caption model, and that the first run may download weights. Two to five minutes before steady caption lines is normal. It is like the first delivery waiting for a driver to reach a new zone. Do not cancel at ninety seconds if the status is already STARTING.

A later job on an instance that is still warm skips the boot and may skip a full image pull. If the image tag moved, it may still download. Watch CloudWatch once the stream exists. Silence, then pull and agent lines, then the model load, then the lines that list photos and write the CSV. A slow first RUNNING is often this stack, not a hung model.

On the screen, a timer stack shows boot, then image pull, then weight download, then inference, and a second job beside it with a shorter stack.

When the status is FAILED, the log line is the source of truth. That is next.
