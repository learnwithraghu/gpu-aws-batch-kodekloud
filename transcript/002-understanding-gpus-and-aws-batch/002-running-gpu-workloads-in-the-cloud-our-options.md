# Video 002 — Running GPU Workloads in the Cloud: Our Options
**Section:** 002 — Understanding GPUs and AWS Batch
**Lecture#:** 002
**Sheet title:** Running GPU Workloads in the Cloud: Our Options
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 002-002-running-gpu-workloads-in-the-c

---

We know we need a GPU and careful micro-batches. In AWS alone there are several places that work could live. Let’s walk the menu with KodeFood’s shape in mind: a containerized job, a folder in, a CSV out, sparse arrivals, no need for an interactive shell.

Amazon EC2 with a GPU instance is the raw building block. You can start a `g4dn`, install drivers, pull an image, run Python, stop the box. Full control, full responsibility. Fine for experiments; noisy for a production queue of vendor folders unless you build your own scheduler.

AWS Lambda is wonderful for short event glue. It is a poor home for a multi-gigabyte CUDA image, a model download, and a multi-minute caption pass. Timeouts, disk, and GPU attachment simply do not match this teaching workload.

Amazon ECS can run GPU tasks if you manage clusters, capacity, and services. Powerful when you already live in ECS. For “run this job when folders appear, then scale toward zero,” you still invent a lot of Batch’s job queue behavior yourself.

Amazon SageMaker shines for managed training and hosted endpoints. You *can* run processing jobs, but for a rare folder-sized inference with a clear start and end, it is often heavier machinery than we need.

AWS Batch sits in the sweet spot for us: submit a container job, let Batch place it on GPU capacity, let capacity fall when the queue drains.

Which option would you defend in a design review? Next we answer directly why this course standardizes on AWS Batch for GPU workloads.

---

## Further reading (not spoken)

- https://docs.aws.amazon.com/batch/latest/userguide/what-is-batch.html — what AWS Batch is for
- https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html — Lambda limits that clash with large GPU containers
- https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html — SageMaker’s broader ML platform scope
