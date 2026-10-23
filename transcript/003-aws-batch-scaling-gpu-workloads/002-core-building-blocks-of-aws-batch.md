# Video 002 — Core Building Blocks of AWS Batch

**Section:** 003 — AWS Batch: Scaling GPU Workloads
**Lecture#:** 002
**Sheet title:** Core Building Blocks of AWS Batch
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 003-002-core-building-blocks-of-aws-ba

---

Batch can feel abstract until you pin it to four pieces.

Think of a busy kitchen. The recipe is the job definition. One plate being cooked is a job. The ticket line is the queue. The kitchen itself — the ovens, burners, and how many cooks can work — is the compute environment.

Why separate those four ideas at all?

Because companies debug them differently. If the recipe is wrong, the dish fails even when the kitchen is ready. If the ticket line is stuck, food never reaches a station. If the kitchen has no capacity, tickets wait even when every recipe is perfect.

For KodeFood, that maps cleanly. A job is one vendor folder to process. The job definition says which container image to run and what resources it needs. The queue holds waiting folders. The compute environment says which GPU machines Batch is allowed to launch, and under what cost and scaling rules.

Uber-style platform thinking uses the same separation: the unit of work, the execution contract, the waiting policy, and the capacity pool are not one blob. Mixing them makes every failure look the same.

So when something breaks, ask which block failed first. Was the work never placeable? Was the recipe asking for the wrong resources? Or did the kitchen simply have no free GPU?

Hold that kitchen model. Next we look closer at the kitchen itself — compute environments on EC2, Fargate, and EKS — and why GPU work usually needs a specific path.

---

## Further reading (not spoken)

- [AWS Batch: Components of AWS Batch](https://docs.aws.amazon.com/batch/latest/userguide/what-is-batch.html#batch_components) — jobs, job definitions, queues, compute environments
- [AWS Batch: Job definitions](https://docs.aws.amazon.com/batch/latest/userguide/job_definitions.html) — the execution recipe
- [AWS Batch: Compute environments](https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html) — the capacity pool
