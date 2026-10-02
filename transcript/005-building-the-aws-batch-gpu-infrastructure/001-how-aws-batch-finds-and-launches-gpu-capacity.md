# Video 001 — How AWS Batch Finds and Launches GPU Capacity

**Section:** 005 — Building the AWS Batch GPU Infrastructure
**Lecture#:** 001
**Sheet title:** How AWS Batch Finds and Launches GPU Capacity
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 005-001-how-aws-batch-finds-and-launch

---

A compute environment is a policy. A waiting job is a request. Now let us follow the point where Batch tries to turn both into a real `g4dn.xlarge`.

You submit the job to a queue bound to one or more compute environments. Batch reads the request: vCPUs, memory, and one GPU. It then asks whether an allowed instance can take it. If desired capacity is zero, Batch raises it and asks EC2 for a matching instance, using the configured capacity type, allowed instance types, subnet, security group, and instance profile.

For Spot, Batch often uses a capacity-optimized allocation strategy. It prefers pools with more spare capacity, but it cannot guarantee a machine. If Spot capacity is thin in the Availability Zone, the launch can fail to place. The job then waits even though the queue is healthy.

On a successful launch, EC2 boots the AMI. The ECS agent registers with the Batch-managed cluster. Only then can Batch place and start the container. From your laptop, this appears as a job changing state. Underneath, the order was scale-up, launch, registration, and placement.

Here is one useful prediction: if the queue is healthy but no Spot instance appears, which job state should you expect to persist? Keep that answer in mind for the lifecycle lesson.

The operating principle is simple: Batch does not already have GPUs. It requests them from EC2 under the rules on the compute environment.

Next, we inspect the AMI and the host-side pieces required before a container can see the GPU.

---

## Further reading (not spoken)

- [AWS Batch: How AWS Batch works](https://docs.aws.amazon.com/batch/latest/userguide/what-is-batch.html) — jobs, queues, compute environments
- [EC2 Spot: Allocation strategies](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-fleet-allocation-strategy.html) — capacity-optimized and related options
- [AWS Batch: Spot best practices](https://docs.aws.amazon.com/batch/latest/userguide/spot_fleet_IAM_role.html) — Spot capacity and Batch
