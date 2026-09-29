# Video 05 — Quotas and cold start
**Type:** Theory
**Runtime target:** ~3 minutes

---

Okay. A service quota is a hard account limit. Here the class is EC2 G and VT capacity, the family that includes g4dn. A VALID compute environment does not override that limit. Batch can only start a g4dn.xlarge if the account may buy that purchase option. get-service-quota is the ground truth.

Spot versus on-demand queues map to two quota codes. Your Spot queue uses L-3819A6DF, All G and VT Spot Instance Requests. Need at least four. This course often has eight. Your on-demand queue uses L-DB2E81BA, Running On-Demand G and VT instances. Need at least four before one g4dn.xlarge can run there. Zero is common on a new account. Then on-demand never starts a container, the job stays RUNNABLE, and /aws/batch/job stays empty. That is not a Python bug.

Check with aws service-quotas get-service-quota, service code ec2, quota code L-DB2E81BA, in the same region as your buckets and compute environment. Same call with L-3819A6DF for Spot. The watch helper picks the code from the compute environment type. Zero means no g4dn will start. Non-zero Spot plus long RUNNABLE is usually capacity in this AZ. If L-DB2E81BA is zero, request an increase in Service Quotas or with request-service-quota-increase, desired value eight. Approval can take hours or days. Until get-service-quota shows at least four, keep BATCH_JOB_QUEUE on Spot. Do not treat on-demand as an automatic escape hatch.

Cold start is different, and it begins only after placement. First job on a fresh instance does three slow things. Instance boots. Agent pulls a multi-gigabyte image from ECR. Container downloads BLIP weights on first use. The program prints Loading caption model. Two to five minutes before steady caption lines is normal. Do not cancel at ninety seconds if status is already STARTING.

A later job on a warm instance skips the boot and may skip a full pull. Watch CloudWatch once the stream exists. Silence, then pull, then model load, then photo lines and the Wrote line with accepted and rejected counts. A slow first RUNNING is often this stack, not a hung model.

When status is FAILED, the log line is the source of truth. That is next.
