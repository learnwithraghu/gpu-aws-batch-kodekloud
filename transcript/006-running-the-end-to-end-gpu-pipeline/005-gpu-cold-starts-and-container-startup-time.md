# Video 005 — GPU Cold Starts and Container Startup Time

**Section:** 006 — Running the End-to-End GPU Pipeline
**Lecture#:** 005
**Sheet title:** GPU Cold Starts and Container Startup Time
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 006-005-gpu-cold-starts-and-container-

---

One of the easiest mistakes in GPU systems is to think, "the job is slow, so the application must be slow."

Very often, that is not true.

Before the real work begins, several startup costs can stack on top of each other. The platform may need to find capacity. A machine may need to launch. A large container image may need to be pulled. Then the model may need to load before the first useful unit of work happens.

That whole gap is what people loosely call a cold start.

In a company setting, this matters because users often experience only the delay, not the reason. They do not care whether the wait came from capacity, image pull, or model initialization. The team has to separate those stages for them.

There is also a cost tradeoff behind the scenes. If you keep GPU capacity warm, startup can feel faster, but you pay for idle hardware. If you scale to zero between bursts, you save money, but the next job pays the startup cost. There is no magic answer. It depends on whether you care more about latency or cost.

That is why cold starts should be understood, not just tolerated. Otherwise every wait gets blamed on the application, when the real cause may be infrastructure startup.

Next, we look at a different kind of delay entirely: a job that is ready in principle, but still cannot get a place to run.

---

## Further reading (not spoken)

- [AWS Batch: Job states — STARTING and RUNNING](https://docs.aws.amazon.com/batch/latest/userguide/job_states.html) — what happens before your code runs
- [Amazon ECR: Image pull performance](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-pull-ecr-image.html) — large image pulls on fresh hosts
- [AWS: Lambda cold starts (contrast)](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtime-environment.html) — same idea, smaller footprint than GPU EC2
