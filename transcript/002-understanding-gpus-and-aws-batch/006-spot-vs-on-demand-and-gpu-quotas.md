# Video 006 — Spot vs On-Demand and GPU Quotas
**Section:** 002 — Understanding GPUs and AWS Batch
**Lecture#:** 006
**Sheet title:** Spot vs On-Demand and GPU Quotas
**Type:** Video
**Runtime target:** ~3 minutes
**Topic code:** 002-006-spot-vs-on-demand-and-gpu-quot

---

We’ve chosen `g4dn.xlarge`. Now we have to decide how AWS Batch acquires that instance—Spot or on-demand—and understand the account quotas that govern both.

Spot instances use spare EC2 capacity at a steep discount, often cutting GPU costs by more than half. For KodeFood’s asynchronous catalog refreshes, Spot is our default path. The tradeoff is availability: if spare T4 capacity is tight in the region, a job waits in `RUNNABLE`, and a running Spot instance can occasionally be interrupted.

On-demand instances pay the standard rate for more predictable capacity. In our setup, we keep a Spot job queue as the primary path and an on-demand job queue as a fallback when timing matters. Switching between them is just a queue name change at job submission.

However, neither queue can launch a `g4dn.xlarge` unless your AWS account has the EC2 Service Quota to allow it. AWS enforces two separate vCPU quotas for the G and VT instance families: one for **All G and VT Spot Instance Requests**, and another for **Running On-Demand G and VT instances**.Because `g4dn.xlarge` has 4 vCPUs, you need a quota of at least 4 vCPUs on whichever path you use.

Here is the trap that catches many engineers on their first GPU project: new AWS accounts frequently start with an on-demand G and VT quota of **zero**. The Batch compute environment and job queue still show `VALID` and `ENABLED`, so everything looks healthy—yet every job submitted to that queue sits in `RUNNABLE` indefinitely. No EC2 instance launches, no container starts, and no CloudWatch logs appear.

That gives us a clean, outside-in debugging rule whenever a GPU job seems stuck:
- If the job stays `RUNNABLE` with no logs, check placement first: Spot capacity, the 12,288 MiB memory ceiling, or your G and VT Service Quotas.
- Only after the job reaches `STARTING` or `RUNNING` should you open CloudWatch `/aws/batch/job` to debug container or Python errors.

Next, we’ll jump into the AWS Console for a live demo and lab to inspect these queues, compute environments, job definition revisions, and GPU quotas firsthand.

---

## Further reading (not spoken)

- https://docs.aws.amazon.com/batch/latest/userguide/spot_fleet_CE_create.html — Spot compute environments in AWS Batch
- https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html — AWS Service Quotas overview
- https://docs.aws.amazon.com/batch/latest/userguide/troubleshooting.html — troubleshooting jobs stuck in `RUNNABLE`
