# Video 006 — Understanding RUNNABLE Jobs and GPU Capacity Problems

**Section:** 006 — Running the End-to-End GPU Pipeline
**Lecture#:** 006
**Sheet title:** Understanding RUNNABLE Jobs and GPU Capacity Problems
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 006-006-understanding-runnable-jobs-an

---

`RUNNABLE` means ready to run, but waiting for a place to run. The caption script is not executing. There is no container yet, so do not start by searching for application logs.

Start with the selected queue and its capacity type. On the default Spot path, `gpu-teaching-gpu-smoke-queue-spot` can be healthy while EC2 has no `g4dn.xlarge` Spot capacity in that Availability Zone. The job waits.

The fallback is not automatically available. On `gpu-teaching-gpu-smoke-queue-on-demand`, Batch still cannot launch a `g4dn.xlarge` if the account's Running On-Demand G and VT instances quota, `L-DB2E81BA`, is zero. In this teaching account it has been zero. The job remains `RUNNABLE`, with no container and no application logs. Use on-demand only after that quota is at least 4. The Spot G and VT quota, `L-3819A6DF`, is 8.

A resource mismatch produces a similar wait. Revision `:1` requests `16384` MiB on a 16 GiB `g4dn.xlarge`, but ECS cannot register all host memory for the task. The status reason is `MISCONFIGURATION:JOB_RESOURCE_REQUIREMENT`. Use `gpu-teaching-caption-job:4` or later with `12288` MiB.

Diagnose in a fixed order. Use `aws batch describe-jobs` or `helpers/watch_batch_job.sh` to read the status reason. Describe the queue and compute environment. Confirm the active job-definition revision, `12288` MiB memory, and one-GPU request. Then check the relevant G and VT quota and current Spot availability. Open `/aws/batch/job` only after the job reaches `STARTING` or `RUNNING`.

You can now distinguish an application failure from a capacity wait: no container means there is no application stack trace yet. With that failure map in place, the next section moves from one vendor folder to production-scale design and utilization.

---

## Further reading (not spoken)

- [AWS Batch: Job states — RUNNABLE](https://docs.aws.amazon.com/batch/latest/userguide/job_states.html) — waiting for capacity
- [AWS Service Quotas: EC2](https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html) — G and VT instance quotas
- [Amazon EC2: Spot best practices](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-best-practices.html) — handling scarce Spot capacity
