# Video 002 — Running GPU Workloads in the Cloud: Our Options
**Section:** 002 — Understanding GPUs and AWS Batch
**Lecture#:** 002
**Sheet title:** Running GPU Workloads in the Cloud: Our Options
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 002-002-running-gpu-workloads-in-the-c

---

We need a GPU and controlled micro-batches. AWS gives us several places to run that work. Let’s compare them against the actual KodeFood shape: a containerized job, one folder in, one CSV out, sparse arrivals, and no interactive shell.

A GPU-backed Amazon EC2 instance is the raw building block. We can start a `g4dn`, install drivers, pull an image, run Python, and stop the instance. That gives us full control and full operational responsibility. It works for experiments. For a queue of vendor folders, we would also need to build scheduling and lifecycle management.

AWS Lambda is useful for short event-driven glue. It does not fit this multi-gigabyte CUDA image, model download, and multi-minute caption pass. Its execution limits and lack of GPU attachment do not match this workload.

Amazon ECS can run GPU tasks while we manage clusters and capacity. It is a strong option when a platform already operates ECS. For this job, we would still need to assemble much of the queue and scale-to-zero behavior around it.

Amazon SageMaker supports managed training, hosted endpoints, and processing jobs. It can run this work, but its broader ML platform is more than we need for occasional folder-sized inference.

AWS Batch matches the shape closely. We submit a container job, Batch places it on GPU capacity, and capacity can fall when the queue drains.

In a design review, the important question is not which service is most capable. It is which service owns the operational work this job actually needs. Next, we’ll make the case for Batch directly.

---

## Further reading (not spoken)

- https://docs.aws.amazon.com/batch/latest/userguide/what-is-batch.html — what AWS Batch is for
- https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html — Lambda limits that clash with large GPU containers
- https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html — SageMaker’s broader ML platform scope
