# Video 008 — Understanding GPU Job Definitions

**Section:** 005 — Building the AWS Batch GPU Infrastructure
**Lecture#:** 008
**Sheet title:** Understanding GPU Job Definitions
**Type:** Video
**Runtime target:** ~3 minutes
**Topic code:** 005-008-understanding-gpu-job-definiti

---

The queue holds the work. The job definition describes what that work needs in order to run correctly.

This is one of the most important Batch concepts because it turns a vague job idea into an explicit execution contract.

In a company, that contract answers questions like these: which packaged application should run, what broad resources does it need, what identity should the workload use, and what default runtime assumptions travel with it?

That is why job definitions matter operationally. If the contract is wrong, the job may wait forever, start without the right access, or run in a way that does not match the workload’s real needs. The scheduler can be healthy and the infrastructure can be available, but a bad execution contract still breaks the outcome.

This also explains why teams treat job-definition revisions carefully. They are not just random versions. They are snapshots of how the workload is expected to run at a point in time. A change in that contract can change placement behavior, permissions, logging, or runtime stability.

So the useful mindset is this: keep the stable execution contract in the job definition, and vary only the small run-specific details elsewhere.

With that, the core infrastructure story is complete. Next, we stop talking about the pieces in isolation and follow a real job from input to result.

---

## Further reading (not spoken)

- [AWS Batch: Job definitions](https://docs.aws.amazon.com/batch/latest/userguide/job_definitions.html) — image, resources, roles, retries
- [AWS Batch: Resource requirements](https://docs.aws.amazon.com/batch/latest/userguide/job_definitions.html#containerproperties.resourceRequirements) — vCPU, memory, GPU
- [Amazon ECS: Memory management](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/memory-management.html) — why host memory is not fully task-available
