# Video 003 — Why AWS Batch for GPU Workloads?
**Section:** 002 — Understanding GPUs and AWS Batch
**Lecture#:** 003
**Sheet title:** Why AWS Batch for GPU Workloads?
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 002-003-why-aws-batch-for-gpu-workload

---

We compared EC2, Lambda, ECS, SageMaker, and Batch. Here is why Batch wins for KodeFood’s caption pipeline.

First, the work is a job, not a server. Each vendor stem is one unit of work with a defined image, CPU, memory, and GPU requirement. You submit; you wait for succeeded or failed; you read the CSV. Batch’s vocabulary matches that mental model.

Second, scale-to-zero matters. Vendor uploads are bursty. Leaving a `g4dn` idle overnight burns money. Batch compute environments in this course set minimum vCPUs to zero so desired capacity can return to nothing when the queue is empty. You pay for the minutes the GPU is needed.

Third, Batch already speaks containers and queues. Our program ships as a Docker image in Amazon ECR. Batch pulls it onto an NVIDIA-ready AMI, attaches one GPU, and runs `python /app/describe_items.py`. We do not SSH in to “just run it once.”

Fourth, overrides keep one image flexible. The same job definition can process `images/sample/` today and another stem tomorrow by changing environment variables at submit time — buckets, prefix, batch size — without rebuilding.

That combination — queued container jobs, GPU placement, and idle capacity that can disappear — is why production teams often pick Batch for offline inference and data processing. Interactive notebooks and always-on APIs can live elsewhere. Batch is not trying to replace every GPU product; it is trying to win this shape of work.

That's it here for the Batch choice: finite GPU jobs, queues, and scale-to-zero when the folder is done. Next we name the four objects you will keep hearing for the rest of the course.

---

## Further reading (not spoken)

- https://docs.aws.amazon.com/batch/latest/userguide/what-is-batch.html — AWS Batch positioning for batch computing
- https://aws.amazon.com/blogs/compute/running-gpu-based-container-applications-with-amazon-ecs-and-aws-batch/ — AWS guidance on GPU containers with Batch
