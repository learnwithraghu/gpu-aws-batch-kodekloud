# Video 003 — Running GPU Workloads in the Cloud: Why AWS Batch?
**Section:** 002 — Understanding GPUs and AWS Batch
**Lecture#:** 003
**Sheet title:** Running GPU Workloads in the Cloud: Why AWS Batch?
**Type:** Video
**Runtime target:** ~3 minutes
**Topic code:** 002-003-running-gpu-workloads-in-the-c

---

We have a containerized job that needs one GPU, processes a folder in micro-batches, writes one CSV to S3, and stops. AWS offers several ways to run containers and ML models, so let’s compare them against that exact shape.

A raw GPU EC2 instance is the basic building block. We can boot a `g4dn`, pull our image, and run the script. That works for a single test, but for a queue of vendor uploads we would have to build our own job queuing, retries, and scale-to-zero lifecycle.

AWS Lambda is great for short event-driven glue, but its runtime limits, storage constraints, and lack of GPU attachment do not fit a multi-gigabyte CUDA container and model pass.

Amazon ECS can run GPU tasks, and Amazon SageMaker provides a full ML platform for training and hosted endpoints. Both can run this code, but with ECS we still assemble the batch queue behavior ourselves, and SageMaker brings more platform surface than we need for a straightforward folder-in, CSV-out container.

AWS Batch matches the KodeFood workload for four reasons.

First, it models a job, not a server. Each vendor folder is one finite unit of work that moves from submitted to succeeded or failed.

Second, it scales to zero. Vendor uploads arrive in bursts, and idle GPUs are expensive. By setting minimum vCPUs to zero on the compute environment, capacity launches when jobs wait in the queue and terminates when the queue drains.

Third, it runs standard Docker images from Amazon ECR on NVIDIA-ready hosts and attaches the requested GPU without manual SSH setup.

Fourth, submit-time overrides keep one container image reusable. The same job definition can process `images/sample/` now and another vendor folder later simply by passing new environment variables for the S3 buckets, prefix, and batch size.

Next, let’s break down the four AWS Batch objects that turn a job submission into a running GPU container.

---

## Further reading (not spoken)

- https://docs.aws.amazon.com/batch/latest/userguide/what-is-batch.html — what AWS Batch is built for
- https://aws.amazon.com/blogs/compute/running-gpu-based-container-applications-with-amazon-ecs-and-aws-batch/ — running GPU containers on AWS Batch
- https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html — Lambda limits for contrast
