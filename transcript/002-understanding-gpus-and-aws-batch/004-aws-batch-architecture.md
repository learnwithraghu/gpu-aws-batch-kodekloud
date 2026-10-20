# Video 004 — AWS Batch Architecture: Jobs, Queues, Compute Environments, and Job Definitions
**Section:** 002 — Understanding GPUs and AWS Batch
**Lecture#:** 004
**Sheet title:** AWS Batch Architecture: Jobs, Queues, Compute Environments, and Job Definitions
**Type:** Video
**Runtime target:** ~3 minutes
**Topic code:** 002-004-aws-batch-architecture--jobs--

---

We chose AWS Batch. Now let’s separate the four objects that make up its architecture and trace how they work together.

Start with the job definition. Think of it as the recipe. It declares the ECR container image, vCPU and memory requirements, GPU count, IAM roles, log configuration, and default command. Whenever we change any of those settings, we register a new revision.

A job is one run of that recipe. When a vendor folder is ready, we submit a job pointing to the job definition and pass runtime overrides like `IMAGE_PREFIX` and `BATCH_SIZE`. Many jobs can share the same definition.

Before a job reaches a machine, it waits in a job queue. Think of the queue as the line. A queue holds waiting jobs—not servers—and routes work to one or more compute environments in priority order.

The compute environment supplies the machines. It defines which EC2 instance types Batch may launch, whether to use Spot or on-demand pricing, the VPC subnet and security group, the EC2 instance profile, and the minimum and maximum vCPU limits. With minimum vCPUs set to zero, an empty queue lets the compute environment scale all the way down.

Notice how permissions split cleanly across this path. The EC2 host uses an instance profile, `ecsInstanceRole`, so the agent can pull the container image from ECR and send logs to CloudWatch. Inside the container, our Python code assumes a separate job role, `gpu-teaching-batch-job-role`, which grants S3 access to read vendor photos and write `descriptions.csv`.

Put the whole flow together: we submit a job to the queue; the compute environment launches a GPU instance with an NVIDIA ECS-optimized AMI; the host pulls the image; the container runs with one GPU and writes the CSV; and when the queue is empty, the instance terminates.

Keep the four-part map handy: the definition is the recipe, the job is one run, the queue is the line, and the compute environment is the kitchen. Next, let’s look closely at the GPU instance inside that kitchen.

---

## Further reading (not spoken)

- https://docs.aws.amazon.com/batch/latest/userguide/job_definitions.html — AWS Batch job definitions
- https://docs.aws.amazon.com/batch/latest/userguide/job_queues.html — AWS Batch job queues
- https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html — AWS Batch compute environments
- https://docs.aws.amazon.com/batch/latest/userguide/jobs.html — AWS Batch jobs and lifecycle states
