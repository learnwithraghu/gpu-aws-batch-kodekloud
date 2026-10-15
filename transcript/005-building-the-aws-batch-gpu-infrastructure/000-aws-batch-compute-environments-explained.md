# Video 000 — AWS Batch Compute Environments Explained

**Section:** 005 — Building the AWS Batch GPU Infrastructure
**Lecture#:** 000
**Sheet title:** AWS Batch Compute Environments Explained
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 005-000-aws-batch-compute-environments

---

We already have the data contract and the container. What is still missing?

A place for the work to run.

That is what a compute environment gives us. In AWS Batch, it defines the pool of machines Batch is allowed to use on our behalf. So instead of humans creating GPU instances whenever work arrives, Batch can grow and shrink capacity using rules we set in advance.

This matters in a real company because GPU time is expensive. Most teams do not want machines sitting idle when no jobs are waiting. They want capacity to appear when needed and disappear when the burst of work is over.

That is exactly the kind of problem a compute environment solves. It expresses the operational policy: what kind of machines are allowed, how much capacity can exist, how the instances are networked, and whether we prefer the cheaper but less predictable path or the steadier but more expensive one.

So think of the compute environment as the infrastructure guardrail around the workload. It does not describe the application logic. It describes the conditions under which that logic is allowed to run.

Next, we follow a waiting job and see how Batch tries to turn those rules into a real GPU machine.

---

## Further reading (not spoken)

- [AWS Batch: Compute environments](https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html) — managed vs unmanaged, scaling knobs
- [Amazon EC2 G4 instances](https://aws.amazon.com/ec2/instance-types/g4/) — T4 GPU shape used in this course
