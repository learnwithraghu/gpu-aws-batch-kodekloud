# Video 001 — How AWS Batch Finds and Launches GPU Capacity

**Section:** 005 — Building the AWS Batch GPU Infrastructure
**Lecture#:** 001
**Sheet title:** How AWS Batch Finds and Launches GPU Capacity
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 005-001-how-aws-batch-finds-and-launch

---

A compute environment is a policy. A waiting job is a request. The interesting moment is when Batch turns that policy into a real `g4dn.xlarge`.

Here is the chain. You submit a job to a queue bound to one or more compute environments. Batch looks at the job’s needs — vCPUs, memory, one GPU — and asks whether an instance can take it. If desired capacity is zero, Batch raises desired capacity and calls EC2 to launch a matching instance: Spot or on-demand, allowed types, subnet, security group, instance profile.

For Spot, Batch often uses a capacity-optimized allocation strategy. That prefers pools with more spare capacity; it does not guarantee a machine. If Spot is thin in the Availability Zone, the launch fails or never places, and your job waits even though the queue is healthy.

On a successful launch, EC2 boots the AMI, the ECS agent registers with the Batch-managed cluster, and only then can the container start. From your laptop it looks like “the job moved.” Underneath it was scale-up, launch, registration, then placement.

Companies that run large Spot GPU fleets live in this same loop: queue depth drives desired capacity, capacity drives EC2, EC2 either appears or it does not. KodeFood’s lesson jobs are small, but the mechanism is identical.

If you remember one sentence from this video, make it this: Batch does not magically have GPUs; it requests them from EC2 under the rules you put on the compute environment.

Next we open the AMI itself — why the NVIDIA ECS-optimized image matters before any container can see a GPU.

---

## Further reading (not spoken)

- [AWS Batch: How AWS Batch works](https://docs.aws.amazon.com/batch/latest/userguide/what-is-batch.html) — jobs, queues, compute environments
- [EC2 Spot: Allocation strategies](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-fleet-allocation-strategy.html) — capacity-optimized and related options
- [AWS Batch: Spot best practices](https://docs.aws.amazon.com/batch/latest/userguide/spot_fleet_IAM_role.html) — Spot capacity and Batch
