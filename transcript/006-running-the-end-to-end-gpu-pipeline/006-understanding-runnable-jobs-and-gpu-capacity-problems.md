# Video 006 — Understanding RUNNABLE Jobs and GPU Capacity Problems

**Section:** 006 — Running the End-to-End GPU Pipeline
**Lecture#:** 006
**Sheet title:** Understanding RUNNABLE Jobs and GPU Capacity Problems
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 006-006-understanding-runnable-jobs-an

---

`RUNNABLE` sounds encouraging, but it often frustrates beginners.

The important meaning is this: the job is ready in theory, but Batch still has nowhere to place it.

That also means the application is not running yet. No container has started. So this is not the moment to begin blaming the code or searching for application logs.

In real teams, `RUNNABLE` usually points to one of a few operational questions. Is GPU capacity actually available? Is the chosen purchase model currently placeable? Is the account allowed to launch that kind of instance? Or did the job ask for a resource profile that does not fit the target machine?

Notice what all of those have in common: they are placement questions, not application questions.

This is one of the biggest mindset shifts in cloud GPU work. A healthy queue does not guarantee a healthy launch. A valid job submission does not guarantee a real machine behind it. GPU systems are constrained by capacity, quotas, and fit much more often than CPU beginners expect.

So diagnose `RUNNABLE` in that order. First ask whether Batch can place the job at all. Only after the job moves into actual startup and execution does application-level debugging become the right next step.

If there is no container yet, there is no application failure yet.

With that distinction in place, we can now zoom out from one job and start thinking about production-scale pipeline design.

---

## Further reading (not spoken)

- [AWS Batch: Job states — RUNNABLE](https://docs.aws.amazon.com/batch/latest/userguide/job_states.html) — waiting for capacity
- [AWS Service Quotas: EC2](https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html) — G and VT instance quotas
- [Amazon EC2: Spot best practices](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-best-practices.html) — handling scarce Spot capacity
