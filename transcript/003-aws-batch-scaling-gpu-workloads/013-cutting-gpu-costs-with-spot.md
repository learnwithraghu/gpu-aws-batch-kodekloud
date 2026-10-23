# Video 013 — Cutting GPU Costs with Spot

**Section:** 003 — AWS Batch: Scaling GPU Workloads
**Lecture#:** 013
**Sheet title:** Cutting GPU Costs with Spot
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 003-013-cutting-gpu-costs-with-spot

---

GPU time is the bill you feel. Spot is how many teams make that bill survivable.

Why accept interruption risk at all?

Because catalog captioning is finite and restartable. If a Spot host disappears mid-job, KodeFood can write outputs to object storage in an idempotent way and let Batch retry. A few extra minutes beats paying full on-demand rates for every vendor folder.

In Batch, Spot shows up as a compute environment purchase option, often with a capacity-optimized allocation strategy so EC2 prefers pools that are less likely to reclaim you immediately. The queue points at that environment. Jobs place when Spot capacity exists.

The operational honesty is this: Spot is not free reliability. Hosts can terminate rudely. Good teams design for that. Keep work units small. Persist progress outside the instance. Configure retries. And keep an on-demand fallback queue for the moments when Spot simply will not place.

DoorDash-like marketplace bursts fit this pattern well. Work arrives in waves. You want cheap GPUs while the wave lasts, then scale toward zero — not a permanent on-demand fleet warming empty seats.

So the mental model is economic resilience, not heroics. Prefer Spot for restartable inference. Fall back when capacity or quotas force your hand.

Next, we close the section by asking how you actually see what is happening — job state, container logs, and whether the GPU is busy or just waiting on data.

---

## Further reading (not spoken)

- [AWS Batch: Spot best practices](https://docs.aws.amazon.com/batch/latest/userguide/spot_fleet_IAM_role.html) — Spot capacity with Batch
- [EC2 Spot: Allocation strategies](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-fleet-allocation-strategy.html) — capacity-optimized placement
- [AWS Batch: Automated job retries](https://docs.aws.amazon.com/batch/latest/userguide/job_retries.html) — retrying after Spot interruption
