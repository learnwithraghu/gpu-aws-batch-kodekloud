# Video 008 — Exploring the AWS Batch GPU Architecture
**Section:** 002 — Understanding GPUs and AWS Batch
**Lecture#:** 008
**Sheet title:** Exploring the AWS Batch GPU Architecture
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 002-008-exploring-the-aws-batch-gpu-ar

---

Let’s pause and assemble everything from this section into one mental map.

KodeFood’s work unit is still a vendor stem: photos under `images/<stem>/`, catalog at `descriptions/<stem>/descriptions.csv`. The program that produces that catalog is a container. Inside it, CPU-side code talks to S3; GPU-side code runs BLIP in micro-batches of eight and marks accepted or rejected.

Around that container sits AWS Batch. The job definition names the image, one GPU, safe memory, and roles. You submit a job with the stem as an override. The job waits in a queue — Spot by default. A managed compute environment may start a `g4dn.xlarge` on an NVIDIA ECS-optimized AMI, but only if quotas and capacity allow. The instance profile pulls from ECR; the job role reaches S3. When the CSV is written and the queue is quiet, capacity can fall toward zero.

If something sticks, use the map. No logs often means the job never left `RUNNABLE` — think Spot scarcity or G/VT quota. A placement error often means memory was set too high for the host. A container exit points you at application logs once the GPU actually ran. Architecture literacy turns those symptoms into short checklists instead of guesswork.

You now have the architecture story without having built the application guts yet. What does the code inside that container actually do, file by file? How is storage logic separated from the model loop?

That question opens section three. Next we start building the GPU application Batch will run — beginning with understanding our program’s entrypoint and responsibilities.

---

## Further reading (not spoken)

- https://docs.aws.amazon.com/batch/latest/userguide/Batch_getting_started.html — getting-started map of Batch components
- https://docs.aws.amazon.com/batch/latest/userguide/gpu-jobs.html — GPU jobs in AWS Batch
