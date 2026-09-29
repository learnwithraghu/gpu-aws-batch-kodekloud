# Video 01 — What AWS Batch is for
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What it is.** **AWS Batch** is a **managed job scheduler** for running **containerized batch work** at scale. You register **what** a job looks like (job definition), **where** it may run (compute environment + queue), and then **submit** individual jobs. Batch integrates with **ECS on EC2** for Docker placement — it is not a separate hypervisor; it is orchestration on top of EC2 capacity you configure.

**Why it exists.** Data and ML teams run millions of **finite tasks**: render frames, score records, convert files, caption photo folders. Those tasks share a pattern — **start, run to completion, exit** — but peak at different times. Batch **queues** work and **scales machines** so you do not leave a GPU server running while a human sleeps, and so you do not manually SSH-launch instances per job like it was 2005.

**Example — contrast three AWS compute stories.** **Interactive notebook on EC2:** you SSH or use Jupyter, iterate for hours, one human drives. **Lambda:** great for seconds-long event handlers, bad for “download ten-gigabyte image, hold T4 for eight minutes.” **Batch:** you build a container once, submit **`jobId` abc** for vendor A and **`jobId` def** for vendor B; each run is tracked, retried, and logged independently — how Procter & Gamble-style nightly pipelines or VFX render farms think about work units.

**In this course.** One job ≈ one vendor folder → one CSV. No SSH into the GPU box; you read **CloudWatch** and **S3** for outcomes.

**Visual:** Three columns — Notebook (human loop), Lambda (short burst), Batch (container queue + scale) — with our catalog job under Batch.

The four named objects Batch uses everywhere — compute environment, queue, job definition, job — come next with a kitchen metaphor.
