# Video 004 — AWS Batch Architecture: Jobs, Queues, Compute Environments and Job Definitions
**Section:** 002 — Understanding GPUs and AWS Batch
**Lecture#:** 004
**Sheet title:** AWS Batch Architecture: Jobs, Queues, Compute Environments and Job Definitions
**Type:** Video
**Runtime target:** ~3 minutes
**Topic code:** 002-004-aws-batch-architecture--jobs--

---

We chose AWS Batch. Now let’s separate its four main objects.

Start with the job definition. Think of it as the recipe. It specifies the container image, CPU and memory, GPU count, permissions, logging, and the default command. In our case, it asks for one GPU and a memory setting that fits the host safely rather than trying to consume the whole machine. When the recipe changes, we register a new revision.

A job is one run of that recipe. We submit “process this stem,” and Batch creates a job with overrides such as the image prefix. Many jobs can use the same definition.

Before a job reaches a machine, it waits in a job queue. Think of the queue as the line. We can use a lower-cost default path and a steadier fallback path. Queue configuration controls priority and which compute environments are available.

The compute environment supplies the machines. It defines allowed instance types, the purchase model, networking, host permissions, and scaling limits. A managed environment lets Batch launch and terminate EC2 capacity. With minimum vCPUs set to zero, an empty queue can allow that capacity to drain.

Let’s trace the normal path. We submit a job to the Spot queue. When its GPU and memory requirements can be placed, the compute environment starts a GPU instance with an NVIDIA ECS-optimized AMI. The agent pulls the image and starts the container with one GPU. The script writes the CSV. When no work remains, desired capacity can fall again.

Once you see these four objects clearly, you can recognize the same queue-plus-worker pattern in many other production batch systems too.

Keep this map handy: the definition is the recipe, the job is one run, the queue is the line, and the compute environment supplies the kitchen.

Next, we’ll choose the GPU instance inside that compute environment and see why a T4 on `g4dn` fits this inference job.

---

## Further reading (not spoken)

- https://docs.aws.amazon.com/batch/latest/userguide/job_definitions.html — job definitions
- https://docs.aws.amazon.com/batch/latest/userguide/job_queues.html — job queues
- https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html — compute environments
- https://docs.aws.amazon.com/batch/latest/userguide/jobs.html — jobs and lifecycle concepts
