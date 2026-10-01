# Video 006 — Spot vs On-Demand GPU Compute
**Section:** 002 — Understanding GPUs and AWS Batch
**Lecture#:** 006
**Sheet title:** Spot vs On-Demand GPU Compute
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 002-006-spot-vs-on-demand-gpu-compute

---

We picked `g4dn.xlarge`. Now the purchase question: Spot or on-demand?

On-demand GPU instances are the straightforward path. You pay the listed price; capacity is more predictable. For a teaching account or a production fallback queue, on-demand is the steady stove.

Spot capacity is unused EC2 offered at a discount. Batch can launch Spot GPU instances for your compute environment and save real money on bursty inference. The tradeoff is availability. Spot may be scarce in a region or get interrupted. A job can sit in `RUNNABLE` for a long time not because your image is broken, but because no Spot `g4dn` showed up.

In this course the default teaching path is Spot. That matches KodeFood’s economics: vendor folders are batch work that can often wait a bit for cheaper capacity. We also keep an on-demand queue in mind as a fallback once the account is allowed to run on-demand G and VT instances.

How should you choose day to day? If a catalog refresh can tolerate delay and you are watching cost, start Spot. If a launch is blocked on capacity or you need a reliable demo in the next few minutes, move to on-demand — after quotas allow it. Many teams keep both queues wired and treat failover as an operational play, not a redesign.

Also remember interruption risk on Spot. A long training job fears reclaim more than our short caption pass does, but you should still design the CSV write to finish cleanly after all photos are described.

That's it here for Spot versus on-demand on GPU: cheaper capacity with interruption risk, versus a steadier price when you cannot wait. But neither model helps if your quotas say zero. Next we face GPU quotas and capacity constraints directly.

---

## Further reading (not spoken)

- https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-spot-instances.html — Spot Instance behavior and interruption model
- https://docs.aws.amazon.com/batch/latest/userguide/spot_fleet_CE_create.html — using Spot with Batch compute environments
