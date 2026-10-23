# Video 001 — How AWS Batch Finds and Launches GPU Capacity

**Section:** 006 — Building the AWS Batch GPU Infrastructure
**Lecture#:** 001
**Sheet title:** How AWS Batch Finds and Launches GPU Capacity
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 006-001-how-aws-batch-finds-and-launch

---

A very important mindset shift happens here.

AWS Batch does not own a shelf of waiting GPUs for your application. It has to go and get capacity from EC2 under the rules you configured.

That means a submitted job kicks off a chain of decisions. Can this request fit the allowed machine types? Is capacity available right now? Can EC2 actually launch the instance? Can that machine come online cleanly enough for the container to be placed?

This is why cloud GPU work feels different from ordinary scripting. The job may be valid and the application may be correct, but the real machine still has to exist before anything useful can happen.

In a company, this is where operators start to distinguish scheduling from execution. If the system cannot find or launch capacity, the application is still innocent. The platform has not even reached the point where the workload can run.

So the big lesson is simple: Batch is a scheduler, not a magic GPU warehouse. It reads the request, asks EC2 for matching capacity, and only then can the workload begin.

Next, we look at one host-side requirement that has to be right before any container can use the GPU at all: the machine image and driver path.

---

## Further reading (not spoken)

- [AWS Batch: How AWS Batch works](https://docs.aws.amazon.com/batch/latest/userguide/what-is-batch.html) — jobs, queues, compute environments
- [EC2 Spot: Allocation strategies](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-fleet-allocation-strategy.html) — capacity-optimized and related options
- [AWS Batch: Spot best practices](https://docs.aws.amazon.com/batch/latest/userguide/spot_fleet_IAM_role.html) — Spot capacity and Batch
