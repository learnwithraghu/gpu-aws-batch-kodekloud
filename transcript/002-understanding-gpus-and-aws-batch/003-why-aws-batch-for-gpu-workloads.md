# Video 003 — Why AWS Batch for GPU Workloads?
**Section:** 002 — Understanding GPUs and AWS Batch
**Lecture#:** 003
**Sheet title:** Why AWS Batch for GPU Workloads?
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 002-003-why-aws-batch-for-gpu-workload

---

We compared EC2, Lambda, ECS, SageMaker, and Batch. For KodeFood, four characteristics make Batch a good fit.

First, this is a job, not a server. Each vendor stem is one unit of work with defined container image, CPU, memory, and GPU requirements. We submit it, wait for a succeeded or failed state, and then read the CSV. Batch’s model matches that lifecycle.

Second, scale-to-zero matters. Vendor uploads are bursty, and an idle `g4dn` still costs money. In this course, the Batch compute environments set minimum vCPUs to zero. When the queue is empty, desired capacity can return to zero.

Third, Batch works with containers and queues. Our program is a Docker image in Amazon ECR. Batch pulls it onto an NVIDIA-ready AMI, attaches one GPU, and runs `python /app/describe_items.py`. There is no SSH step in the normal job path.

Fourth, submit-time overrides keep one image reusable. The same job definition can process `images/sample/` today and a different stem tomorrow. We change environment variables for buckets, prefix, and batch size without rebuilding the image.

The result is a focused platform for finite GPU work: queued containers, GPU placement, and capacity that can disappear when the work is done. Interactive notebooks and always-on APIs solve different problems.

Next, let’s name the four Batch objects that carry this job from submission to completion.

---

## Further reading (not spoken)

- https://docs.aws.amazon.com/batch/latest/userguide/what-is-batch.html — AWS Batch positioning for batch computing
- https://aws.amazon.com/blogs/compute/running-gpu-based-container-applications-with-amazon-ecs-and-aws-batch/ — AWS guidance on GPU containers with Batch
