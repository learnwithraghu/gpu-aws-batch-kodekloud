# Video 003 — When AWS Batch Is the Right Choice — and When It Isn't

**Section:** 007 — Production GPU Pipeline Design
**Lecture#:** 003
**Sheet title:** When AWS Batch Is the Right Choice — and When It Isn't
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 007-003-when-aws-batch-is-the-right

---

Batch earned its place in this course for a specific shape of work. You have a queue of independent units — one vendor folder each. You want containers with GPUs. You want AWS to launch capacity when jobs appear and scale toward zero when the queue drains. You can tolerate minutes of cold start. Retries and Spot interruptions are acceptable if a failed stem can re-run cleanly. That is KodeFood captioning. That is also a lot of overnight analytics, rendering, and batch inference in the wild.

When is Batch the wrong hammer? Synchronous APIs — “caption this photo in 200 milliseconds” — need a warm service on ECS, EKS, or a managed endpoint, not a cold job boot. If your org already runs on Kubernetes operators and GitOps, pure EKS may fit the operating model better. If data scientists need managed training loops, experiments, and built-in metrics, SageMaker Training is often the shorter path.

AWS’s own guidance is blunt: Fargate is simpler until you need GPUs — and GPU Batch jobs need EC2-backed environments. “Serverless-looking” does not mean Fargate for this workload. “ML on AWS” does not automatically mean SageMaker when you already have a container and a queue.

Batch case studies on AWS’s site rhyme: large volumes of similar jobs, Spot-friendly cost, operators who want scheduling without owning a cluster day-to-day. Match that pattern and Batch pays off. Fight it and you will wrestle RUNNABLE states forever.

Ask yourself one sentence: is this work a job or a service? Next we put Batch beside ECS, EKS, and SageMaker so that sentence gets sharper.

---

## Further reading (not spoken)

- [What is AWS Batch?](https://docs.aws.amazon.com/batch/latest/userguide/what-is-batch.html) — intended use: managed batch compute on ECS/EKS
- [AWS Batch: When to use Fargate](https://docs.aws.amazon.com/batch/latest/userguide/bestpractice4.html) — EC2 required when you need GPUs
- [AWS Batch customer stories](https://aws.amazon.com/batch/) — production batch patterns across industries
