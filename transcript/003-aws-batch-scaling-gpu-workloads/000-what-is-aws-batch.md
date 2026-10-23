# Video 000 — What Is AWS Batch?

**Section:** 003 — AWS Batch: Scaling GPU Workloads
**Lecture#:** 000
**Sheet title:** What Is AWS Batch?
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 003-000-what-is-aws-batch

---

We already know why GPUs matter for KodeFood. Vendor photos need parallel model work, and that work arrives in bursts.

So why introduce another AWS service at all? Why not just keep a GPU machine running and process folders as they arrive?

Because idle GPUs are expensive, and bursty catalog work does not need a permanent machine. When a vendor folder lands, you want capacity to appear. When the queue is empty, you want that capacity to disappear. That is the operational tension Batch is built for.

AWS Batch is a managed job scheduler for finite container workloads. You submit work. Batch decides when and where it can run. It asks EC2 for matching capacity, places the container, and can scale the fleet back toward zero when nothing is waiting.

That is different from treating Batch as “the application.” The application is still the logic that turns images into a catalog CSV. Batch is the control plane around it: queues, placement rules, and capacity policy.

Netflix-style offline scoring systems follow a similar pattern. Heavy model work runs as a dedicated batch step so the customer-facing product can read prepared results quickly, instead of keeping expensive accelerators warm all day.

For KodeFood, that means one clear operating idea. Folders arrive. Jobs wait. GPUs appear only while work exists. Then the bill goes quiet again.

Next, we compare Batch with the services people often reach for first: raw EC2, Lambda, and ECS.

---

## Further reading (not spoken)

- [What is AWS Batch?](https://docs.aws.amazon.com/batch/latest/userguide/what-is-batch.html) — managed batch compute for container jobs
- [AWS Batch: How AWS Batch works](https://docs.aws.amazon.com/batch/latest/userguide/what-is-batch.html#how_it_works) — jobs, queues, and compute environments
- [Netflix Technology Blog: Machine Learning](https://netflixtechblog.com/) — offline batch scoring patterns vs always-on serving
