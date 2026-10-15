# Video 008 — Exploring the AWS Batch GPU Architecture
**Section:** 002 — Understanding GPUs and AWS Batch
**Lecture#:** 008
**Sheet title:** Exploring the AWS Batch GPU Architecture
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 002-008-exploring-the-aws-batch-gpu-ar

---

Let’s assemble the section into one path.

KodeFood’s work unit is a vendor stem. Photos live under one input prefix, and the catalog is written to one output CSV. A container produces that catalog. Inside it, CPU-side code communicates with S3, GPU-side code runs BLIP in micro-batches, and application logic marks each caption accepted or rejected.

AWS Batch surrounds that container. The job definition specifies the image, resource shape, and roles. We submit a job with the vendor stem as an override, and it waits in a queue. If quotas and capacity allow, the managed compute environment starts the GPU instance and the container can run.

The instance profile lets the host pull from ECR and write logs. The job role lets the container reach S3. After the CSV is written and the queue becomes quiet, capacity can fall toward zero.

When something stalls, trace the path in order. No logs often means the job never left `RUNNABLE`; check Spot capacity and G/VT quota. A placement error often points to a memory request that is too large for the host. A container exit means the machine started, so application logs are now the right place to look.

That outside-in debugging order is how experienced teams avoid wasting time on code when the workload never even reached a machine.

That gives us the architecture without hiding the failure boundaries. The remaining question is what the code inside the container does, file by file, and how it separates storage from the model loop.

Section three starts there. We’ll open the application at its entrypoint and trace each responsibility.

---

## Further reading (not spoken)

- https://docs.aws.amazon.com/batch/latest/userguide/Batch_getting_started.html — getting-started map of Batch components
- https://docs.aws.amazon.com/batch/latest/userguide/gpu-jobs.html — GPU jobs in AWS Batch
