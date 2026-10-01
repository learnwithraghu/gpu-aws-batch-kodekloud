# Video 006 — Understanding RUNNABLE Jobs and GPU Capacity Problems

**Section:** 006 — Running the End-to-End GPU Pipeline
**Lecture#:** 006
**Sheet title:** Understanding RUNNABLE Jobs and GPU Capacity Problems
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 006-006-understanding-runnable-jobs-an

---

RUNNABLE means “ready to run, waiting for a place to run.” It does not mean your caption script is executing. There is no container yet, so there are no application logs to chase.

Two capacity stories dominate our teaching account. Spot: the queue is healthy, the job definition is fine, but EC2 has no `g4dn.xlarge` Spot capacity in that zone right now. The job waits. On-demand: if the account’s Running On-Demand G and VT instances quota is zero, Batch cannot launch the fallback instance either — RUNNABLE forever with a quiet log group.

A third cousin looks similar: the job asks for more memory than the instance can register. Sixteen gibibytes on a sixteen-gibibyte `g4dn.xlarge` yields a resource misconfiguration and never places. That is why the caption definition stays at twelve thousand two hundred eighty-eight MiB.

How do you debug without guessing? Check Service Quotas for G and VT Spot and on-demand. Describe the compute environment and queue. Confirm the job definition revision and memory. Use a watch helper or `describe-jobs` for status reason. Only after the job reaches STARTING or RUNNING do you open `/aws/batch/job`.

GPU scarcity is not unique to this course. Hyperscalers and startups alike report Spot interruptions and quota walls on G-family capacity. The skill is recognizing RUNNABLE as a capacity signal, not an application stack trace.

You can now walk KodeFood from prefix to SUCCEEDED — and explain the waits. Section seven zooms out to production design: scaling from one vendor folder to many jobs, utilization, and when Batch is the right tool versus adjacent AWS GPU options.

---

## Further reading (not spoken)

- [AWS Batch: Job states — RUNNABLE](https://docs.aws.amazon.com/batch/latest/userguide/job_states.html) — waiting for capacity
- [AWS Service Quotas: EC2](https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html) — G and VT instance quotas
- [Amazon EC2: Spot best practices](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-best-practices.html) — handling scarce Spot capacity
