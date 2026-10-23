# Video 014 — Monitoring Batch Jobs and GPU Usage

**Section:** 003 — AWS Batch: Scaling GPU Workloads
**Lecture#:** 014
**Sheet title:** Monitoring Batch Jobs and GPU Usage
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 003-014-monitoring-batch-jobs-and-gpu-

---

When a GPU job “feels slow,” the first question is not “is Python slow?”

The first question is which layer you are looking at.

Batch exposes a control-plane story: submitted, runnable, starting, running, succeeded, or failed. Runnable means the scheduler still has nowhere to place the job. There is no container yet, so there are no application logs yet. Running means placement succeeded and the workload can actually print something useful.

Only after the job is running do container logs in the Batch log group become the right next stop. That is where you see model load, image downloads, and caption progress. Confusing those two layers is how teams waste an hour hunting bugs that do not exist yet.

There is a third lens: is the GPU actually busy? A job can be running while the accelerator sits nearly idle because the bottleneck is CPU preprocessing or object-storage downloads. Utilization metrics and host tools answer that question. Logs alone will not.

So build a short diagnostic habit. State first. Logs second. Utilization third. Each answer points to a different fix — capacity, application, or data path.

That closes the Batch concepts arc for this section. The last console demo puts GPU Spot into practice — inspect the live GPU kitchen, run a smoke job, and watch placement. After that, we leave the scheduler alone for a moment and open the KodeFood application itself — what the container program actually does with a vendor folder.

---

## Further reading (not spoken)

- [AWS Batch: Job states](https://docs.aws.amazon.com/batch/latest/userguide/job_states.html) — control-plane lifecycle including RUNNABLE
- [AWS Batch: CloudWatch Logs](https://docs.aws.amazon.com/batch/latest/userguide/using_cloudwatch_logs.html) — container log configuration
- [Amazon CloudWatch: Container Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ContainerInsights.html) — utilization views beyond job status
