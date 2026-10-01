# Video 008 — Understanding GPU Job Definitions

**Section:** 005 — Building the AWS Batch GPU Infrastructure
**Lecture#:** 008
**Sheet title:** Understanding GPU Job Definitions
**Type:** Video
**Runtime target:** ~3 minutes
**Topic code:** 005-008-understanding-gpu-job-definiti

---

The queue holds the wait. The job definition holds the contract for what runs when capacity appears. Think of it as the recipe card Batch hands the container runtime.

For KodeFood’s caption job, that recipe includes the ECR image URI, resource requirements, the job role, environment variables, and logging. Resource requirements are where GPU jobs get specific: you ask for vCPUs, memory in MiB, and one GPU. Our live definition uses twelve thousand two hundred eighty-eight MiB — twelve gigabytes of memory — not sixteen. A `g4dn.xlarge` advertises sixteen GiB of instance memory, but ECS does not register the full amount for your task. Ask for sixteen thousand three hundred eighty-four MiB and the job can sit forever with a resource misconfiguration. That is a real teaching-account footgun, not a theoretical one.

The job role ARN belongs on the definition so the container can read and write S3. Skip it and the instance may still pull from ECR while the Python process dies on AccessDenied. Environment variables carry default bucket names. Explicit `awslogs` configuration sends stdout to the `/aws/batch/job` log group so you are not hunting for streams. The default command on the definition can be a tiny smoke check; at submit time you override it to `python /app/describe_items.py` with the prefix you care about.

Every `register-job-definition` call creates a new revision. Submit by name and Batch uses the latest active revision unless you pin one. Old revisions without a job role or with wrong memory still exist in history — which is why “it worked last week” can mean “you are not on the revision you think.” Pin a known-good revision for lessons when you need to be sure.

Production teams version job definitions the way they version deployment specs. Databricks-style and internal Batch platforms treat the definition as the immutable unit of “what this workload is,” then vary only overrides per run. Treat image URI changes the same way: rebuild and push first, then confirm the definition still points at the tag or digest you intend.

You now have the infrastructure set: compute environment, AMI, IAM, network, queue, and job definition. Section six is where we run the pipeline end to end — from an S3 input prefix through submit, lifecycle states, overrides, cold starts, and the RUNNABLE traps that look like application bugs but are not.

---

## Further reading (not spoken)

- [AWS Batch: Job definitions](https://docs.aws.amazon.com/batch/latest/userguide/job_definitions.html) — image, resources, roles, retries
- [AWS Batch: Resource requirements](https://docs.aws.amazon.com/batch/latest/userguide/job_definitions.html#containerproperties.resourceRequirements) — vCPU, memory, GPU
- [Amazon ECS: Memory management](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/memory-management.html) — why host memory is not fully task-available
