# Video 000 — Reviewing the Complete Production Architecture

**Section:** 007 — Production GPU Pipeline Design
**Lecture#:** 000
**Sheet title:** Reviewing the Complete Production Architecture
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 007-000-reviewing-the-complete-product

---

In the last section you watched a job sit in RUNNABLE. That feeling — ready work, no GPU yet — is not a side quest. It is the production signal. Capacity is scarce, Spot comes and goes, quotas gate on-demand, and cold starts take minutes. So this section asks a different question: given those constraints, is the KodeFood architecture shaped for production, or did we only prove one happy path?

Start with the pieces you already built, end to end. Vendor photos land under an S3 prefix — `images/<stem>/`. A container image in Amazon ECR holds the caption program: list, download, BLIP inference, accept or reject, write `descriptions.csv`. AWS Batch owns the four objects: compute environment, queue, job definition, and the job you submit with overrides for that stem. CloudWatch `/aws/batch/job` is where the container truth lives when exit code 1 appears.

Notice the design choices that matter under pressure. Storage is not glued inside the model file — S3 is the contract. The GPU is not always-on — `minvCpus` at zero means you pay for work, not for an idle g4dn waiting for the next vendor. Spot is the default path; on-demand is the fallback when RUNNABLE goes quiet. Memory on the job definition is sized to place, not to impress — 12288 MiB on `g4dn.xlarge`, not 16384.

That pattern shows up outside this course. Marketplace photo pipelines and media encoding farms treat images as durable objects and models as replaceable workers — queue independent units instead of keeping every encoder hot. Durable inputs, ephemeral GPU, one artifact out.

That's it here for the production picture: S3 in, ECR image, Batch queue and GPU CE, CSV out, then scale to zero. The next pressure is volume — how we go from one vendor folder to thousands of jobs without rewriting the application.

---

## Further reading (not spoken)

- [AWS Batch User Guide](https://docs.aws.amazon.com/batch/) — jobs, queues, compute environments, and job definitions
- [AWS Batch: Best practices](https://docs.aws.amazon.com/batch/latest/userguide/bestpractices.html) — sizing, Spot, and operational guidance
