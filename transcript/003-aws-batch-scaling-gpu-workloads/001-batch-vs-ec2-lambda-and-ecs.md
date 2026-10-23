# Video 001 — Batch vs EC2, Lambda, and ECS

**Section:** 003 — AWS Batch: Scaling GPU Workloads
**Lecture#:** 001
**Sheet title:** Batch vs EC2, Lambda, and ECS
**Type:** Video
**Runtime target:** ~3 minutes
**Topic code:** 003-001-batch-vs-ec2-lambda-and-ecs

---

If Batch is a scheduler for finite GPU jobs, why not just launch an EC2 GPU instance yourself?

That is the naive path many teams try first. It works for a demo. It gets painful in production.

Raw EC2 puts the human in charge of capacity. Someone has to start the machine, place the container, watch for failures, and remember to stop the instance when the burst is over. Miss that last step, and the GPU keeps billing overnight for zero catalog value.

Lambda feels attractive for “event in, function out,” but it is the wrong shape for KodeFood. Heavy model containers, long startup, and GPU requirements sit outside what Lambda is designed to host cleanly. You would be forcing a batch inference problem into a request-function product.

ECS is closer. It runs containers well, and many companies use it for long-lived services. The difference is intent. ECS shines when you want a service that stays available. Batch shines when you want a queue of finite jobs, with capacity that grows and shrinks under scheduling rules instead of under constant human babysitting.

Uber’s public ML platform writing makes a related point: keep units of work small, restartable, and separate from always-on product serving. That is the same boundary we are drawing here.

So the comparison is not “which service is best.” It is “which abstraction matches the work.” KodeFood needs one folder processed, one result written, and no GPU bill when the queue is empty. That is Batch territory.

ECS can still appear underneath. In this course, Batch often uses ECS orchestration to place containers on the machines it launches. Batch adds the job queue, the placement policy, and the scale-to-zero behavior around that.

Keep one diagnostic question ready: are we operating a service that must stay warm, or a job that should exist only while work is waiting?

Next, we name the four building blocks Batch uses to turn that idea into something you can operate.

---

## Further reading (not spoken)

- [AWS Batch: What is AWS Batch?](https://docs.aws.amazon.com/batch/latest/userguide/what-is-batch.html) — when Batch is the intended abstraction
- [Amazon ECS vs AWS Batch](https://docs.aws.amazon.com/batch/latest/userguide/what-is-batch.html) — Batch as a scheduler on top of container orchestration
- [AWS Lambda quotas and limits](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html) — why large GPU model containers are a poor Lambda fit
- [Uber Engineering: Michelangelo](https://www.uber.com/blog/michelangelo-machine-learning-platform/) — small, restartable ML work units vs always-on serving
