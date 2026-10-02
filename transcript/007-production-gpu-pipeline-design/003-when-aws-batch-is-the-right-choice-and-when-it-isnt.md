# Video 003 — When AWS Batch Is the Right Choice — and When It Isn't

**Section:** 007 — Production GPU Pipeline Design
**Lecture#:** 003
**Sheet title:** When AWS Batch Is the Right Choice — and When It Isn't
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 007-003-when-aws-batch-is-the-right

---

Batch fits this course because the work has a clear shape. Each vendor folder is independent. The container needs a GPU, but it does not need one permanently. Capacity can launch when jobs arrive and return toward zero when the queue drains. A few minutes of startup is acceptable, and a failed stem can run again after a Spot interruption. KodeFood captioning fits that profile, as do many rendering, analytics, and batch-inference systems.

Batch is a poor fit for a synchronous request such as “caption this photo in 200 milliseconds.” That requires a warm service on ECS, EKS, or a managed endpoint. An organization already operating Kubernetes through operators and GitOps may prefer EKS. A team that needs managed training loops, experiments, and built-in metrics may reach production faster with SageMaker Training.

One platform constraint is easy to miss: GPU Batch jobs require an EC2-backed compute environment. Fargate may simplify CPU workloads, but it is not the GPU path here. Likewise, an ML workload does not automatically require SageMaker when the real need is to schedule an existing container.

The successful Batch pattern is consistent: many similar jobs, tolerance for Spot economics, and a team that wants scheduling without operating a cluster day to day. If a design requires permanently warm capacity or request-level latency, repeated RUNNABLE incidents are a symptom of the wrong abstraction.

Use one review question: is this work a finite job or a continuously available service? Next we compare Batch, ECS, EKS, and SageMaker with that boundary in mind.

---

## Further reading (not spoken)

- [What is AWS Batch?](https://docs.aws.amazon.com/batch/latest/userguide/what-is-batch.html) — intended use: managed batch compute on ECS/EKS
- [AWS Batch: When to use Fargate](https://docs.aws.amazon.com/batch/latest/userguide/bestpractice4.html) — EC2 required when you need GPUs
- [AWS Batch customer stories](https://aws.amazon.com/batch/) — production batch patterns across industries
