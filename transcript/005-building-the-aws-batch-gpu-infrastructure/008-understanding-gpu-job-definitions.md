# Video 008 — Understanding GPU Job Definitions

**Section:** 005 — Building the AWS Batch GPU Infrastructure
**Lecture#:** 008
**Sheet title:** Understanding GPU Job Definitions
**Type:** Video
**Runtime target:** ~3 minutes
**Topic code:** 005-008-understanding-gpu-job-definiti

---

The queue holds the waiting job. The job definition describes exactly what should run when capacity appears. It is the contract Batch hands to the container runtime.

For KodeFood, that contract includes the ECR image URI, resource requirements, job role, environment variables, and logging. The GPU resource request names vCPUs, memory in MiB, and one GPU.

Pay close attention to memory. The live definition uses `12288` MiB, not `16384` MiB. A `g4dn.xlarge` has 16 GiB of instance memory, but ECS does not register all of it for the task because the operating system and agent need memory too. A request for `16384` MiB produces `MISCONFIGURATION:JOB_RESOURCE_REQUIREMENT` and never places. Use revision `:4` or later, with `12288` MiB.

The `jobRoleArn` belongs on the definition so the container can read and write S3. If it is absent, the instance can still pull from ECR while Python fails with `AccessDenied`. Environment variables carry the default bucket names. Explicit `awslogs` configuration sends stdout to `/aws/batch/job`. The default command can be a small smoke check; at submission time, we override it with `python /app/describe_items.py` and the required prefix.

Every `register-job-definition` call creates a revision. Submitting by name uses the latest active revision unless you pin one. Revision `:1` asks for `16384` MiB and is broken. Revision `:2` has no `jobRoleArn`. Revision `:3` has the job role but no explicit log configuration. Revision `:4` has `12288` MiB, the job role, and explicit `awslogs`. Pin a known-good revision when the lab must be deterministic.

Treat the definition as the stable workload specification, and vary only the intended per-run overrides. When application files change, remember that Batch runs the baked image: rebuild and push first, then confirm the definition still points to the intended tag or digest.

The infrastructure contract is now complete: compute environment, AMI, IAM, network, queue, and job definition. In the next section, we follow a real S3 prefix through submission, lifecycle states, overrides, cold start, and the `RUNNABLE` failure modes that occur before application code runs.

---

## Further reading (not spoken)

- [AWS Batch: Job definitions](https://docs.aws.amazon.com/batch/latest/userguide/job_definitions.html) — image, resources, roles, retries
- [AWS Batch: Resource requirements](https://docs.aws.amazon.com/batch/latest/userguide/job_definitions.html#containerproperties.resourceRequirements) — vCPU, memory, GPU
- [Amazon ECS: Memory management](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/memory-management.html) — why host memory is not fully task-available
