# Video 000 — Reviewing the Complete Production Architecture

**Section:** 007 — Production GPU Pipeline Design
**Lecture#:** 000
**Sheet title:** Reviewing the Complete Production Architecture
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 007-000-reviewing-the-complete-product

---

In the last section, you saw a job remain RUNNABLE because no GPU was available. In a design review, we would not dismiss that as a lab inconvenience. It is an operating condition. Capacity changes, quotas can block launches, and cold starts can take minutes. The production question is whether the KodeFood design behaves predictably under those constraints.

Trace the system from input to output. Vendor photos arrive in S3. The image in ECR contains the caption program. AWS Batch connects the compute environment, queue, job definition, and submitted job. The selected vendor stem arrives at runtime. If the container exits after startup, begin the incident review in CloudWatch logs.

Now check the choices that reduce blast radius and idle cost. S3 is the durable contract; the model container is replaceable. With scale-to-zero, the GPU fleet can disappear when the queue is empty. Spot is the normal path. On-demand is only the fallback when the account can actually launch it. The job definition also has to fit the instance cleanly, or placement fails before the application ever begins.

This is the same pattern used in photo processing and media encoding: durable inputs, independent work items, ephemeral workers, and one durable result. During review, ask one diagnostic question: if this container disappears halfway through a folder, can we rerun the same stem without repairing state by hand?

That pattern keeps showing up in real systems because it makes retries cheaper, failures smaller, and idle cost easier to control.

That is the production baseline: S3 in, an ECR image on Batch, a CSV out, then scale to zero. Next we apply the same shape to thousands of vendor folders.

---

## Further reading (not spoken)

- [AWS Batch User Guide](https://docs.aws.amazon.com/batch/) — jobs, queues, compute environments, and job definitions
- [AWS Batch: Best practices](https://docs.aws.amazon.com/batch/latest/userguide/bestpractices.html) — sizing, Spot, and operational guidance
