# Video 004 — AWS Batch Architecture: Jobs, Queues, Compute Environments and Job Definitions
**Section:** 002 — Understanding GPUs and AWS Batch
**Lecture#:** 004
**Sheet title:** AWS Batch Architecture: Jobs, Queues, Compute Environments and Job Definitions
**Type:** Video
**Runtime target:** ~3 minutes
**Topic code:** 002-004-aws-batch-architecture--jobs--

---

We chose AWS Batch. Now let’s name the four objects so they stop blending together.

Start with the job definition. Think of it as the recipe. It pins the container image — for us, the GPU teaching image in ECR — plus vCPUs, memory, GPU count, the job role that may read and write S3, logging configuration, and the default command. Our live recipe asks for one GPU and twelve thousand two hundred eighty-eight MiB of memory, not the full sixteen gibibytes of a `g4dn.xlarge`, because the host needs room for the operating system and the ECS agent. Register a definition once; revise it when the recipe changes.

Next is the job. A job is one cook of that recipe. You submit “process this stem,” and Batch creates a job with overrides for environment variables like the image prefix. Many jobs can share one definition.

Jobs do not jump straight onto machines. They wait in a job queue. The queue is the line. You can have a Spot queue as the default cheap path and an on-demand queue as a steadier fallback. Priority and which compute environments the queue may use are bound here.

The compute environment is the kitchen that can appear and disappear. It declares which instance types are allowed — we focus on `g4dn.xlarge` — Spot or on-demand, networking, the instance profile that pulls from ECR and writes logs, and how far capacity may scale. Managed environments let Batch launch and terminate EC2 capacity for you. With minimum vCPUs at zero, an empty queue can drain the kitchen lights.

Let’s trace one happy path. You submit a job to the Spot queue. The job becomes runnable when the definition’s GPU and memory requirements can be placed. The compute environment starts a GPU instance with an NVIDIA ECS-optimized AMI. The agent pulls the image, starts the container with one GPU, and your script writes the CSV. When nothing else is waiting, desired capacity can fall again.

If you remember only one sentence: definition is the recipe, job is one run, queue is the line, compute environment is the kitchen. Keep that map handy — we will hang instance choice, Spot, and quotas on it next.

How do you pick the stove inside that kitchen? Next we look at GPU EC2 families and why a T4 on `g4dn` fits this inference job.

---

## Further reading (not spoken)

- https://docs.aws.amazon.com/batch/latest/userguide/job_definitions.html — job definitions
- https://docs.aws.amazon.com/batch/latest/userguide/job_queues.html — job queues
- https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html — compute environments
- https://docs.aws.amazon.com/batch/latest/userguide/jobs.html — jobs and lifecycle concepts
