# Video 006 — Spot vs On-Demand GPU Compute
**Section:** 002 — Understanding GPUs and AWS Batch
**Lecture#:** 006
**Sheet title:** Spot vs On-Demand GPU Compute
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 002-006-spot-vs-on-demand-gpu-compute

---

We’ve chosen `g4dn.xlarge`. Now we need a purchase model: Spot or on-demand.

On-demand GPU instances use the listed price and generally offer more predictable access to capacity. That makes an on-demand queue useful when timing matters or as a production fallback.

Spot uses spare EC2 capacity at a discount. Batch can launch Spot GPU instances for bursty inference, but availability is not guaranteed. Capacity may be scarce in a region, and running instances can be interrupted. A job may sit in `RUNNABLE` because no Spot `g4dn` is available—not because the image is broken.

This course starts with Spot. KodeFood’s vendor folders are batch work and can usually wait for lower-cost capacity. We keep an on-demand queue as a fallback once the account is allowed to run on-demand G and VT instances.

For daily decisions, start with the workload deadline. If a catalog refresh can wait, Spot is reasonable. If capacity delay blocks a launch or time-sensitive demonstration, use on-demand after confirming the quota. Keeping both queues available turns that switch into an operational choice instead of an architecture change.

Spot interruption still matters. Our short caption pass has less exposure than a long training job, but the CSV should only be finalized after all photos are described.

Purchase choice is only half the capacity story. Next, let’s inspect the quotas and regional constraints that can prevent either path from launching.

---

## Further reading (not spoken)

- https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-spot-instances.html — Spot Instance behavior and interruption model
- https://docs.aws.amazon.com/batch/latest/userguide/spot_fleet_CE_create.html — using Spot with Batch compute environments
