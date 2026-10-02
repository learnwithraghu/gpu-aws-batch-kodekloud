# Video 000 — Reviewing the Complete Production Architecture

**Section:** 007 — Production GPU Pipeline Design
**Lecture#:** 000
**Sheet title:** Reviewing the Complete Production Architecture
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 007-000-reviewing-the-complete-product

---

In the last section, you saw a job remain RUNNABLE because no GPU was available. In a design review, we would not dismiss that as a lab inconvenience. It is an operating condition: Spot capacity changes, quotas can block on-demand instances, and a cold start can take minutes. The production question is whether the KodeFood design behaves predictably under those constraints.

Trace the system from input to output. Vendor photos arrive at `images/<stem>/` in S3. The image in Amazon ECR contains the caption program: list the files, download them, run BLIP inference, accept or reject each result, and write `descriptions.csv`. AWS Batch connects the compute environment, queue, job definition, and submitted job. The stem arrives as an override. If the container exits with code 1, start the incident review in CloudWatch at `/aws/batch/job`.

Now check the choices that reduce blast radius and idle cost. S3 is the durable contract; the model container is replaceable. With `minvCpus` set to zero, the GPU fleet can disappear when the queue is empty. Spot is the normal path. On-demand can serve as the capacity fallback only after the account’s G and VT quota reaches at least four vCPUs. The job requests 12288 MiB on `g4dn.xlarge`, because 16384 MiB cannot be placed on that instance after system overhead.

This is the same pattern used in photo processing and media encoding: durable inputs, independent work items, ephemeral workers, and one durable result. During review, ask one diagnostic question: if this container disappears halfway through a folder, can we rerun the same stem without repairing state by hand?

That is the production baseline: S3 in, an ECR image on Batch, a CSV out, then scale to zero. Next we apply the same shape to thousands of vendor folders.

---

## Further reading (not spoken)

- [AWS Batch User Guide](https://docs.aws.amazon.com/batch/) — jobs, queues, compute environments, and job definitions
- [AWS Batch: Best practices](https://docs.aws.amazon.com/batch/latest/userguide/bestpractices.html) — sizing, Spot, and operational guidance
