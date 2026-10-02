# Video 005 — GPU Cold Starts and Container Startup Time

**Section:** 006 — Running the End-to-End GPU Pipeline
**Lecture#:** 005
**Sheet title:** GPU Cold Starts and Container Startup Time
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 006-005-gpu-cold-starts-and-container-

---

The job is correctly submitted, but several minutes pass before BLIP writes its first log line. That gap is a cold start, and on GPU Batch it is usually several waits stacked together.

First, the compute environment may be at zero. EC2 must find and launch a `g4dn.xlarge`, boot the NVIDIA ECS-optimized AMI, and register the ECS agent. Spot capacity can add minutes to this stage.

Second, the container image pulls from ECR. The teaching image is multi-gigabyte and contains CUDA, PyTorch, transformers, and the application. A first pull on a fresh instance can dominate startup time. A later job on a warm host may reuse layers.

Third, the process starts and loads the model. BLIP weights move into GPU memory before photo iteration begins. If those weights download on first use, network transfer adds another delay.

There is a direct cost trade-off. Keeping `minvCpus` above zero can hide AMI boot time, but it pays for an idle GPU. This course keeps `minvCpus` at zero to control the teaching bill, so the lab exposes the full cold path.

In the lab, measure two intervals: submission until the job reaches `RUNNING`, then `RUNNING` to the first caption log. The first interval is dominated by capacity and startup. The second exposes model initialization and application work.

That separates AMI boot, image pull, and model load instead of assigning the entire delay to `describe_items.py`. Next, we investigate the more serious symptom: a job that never leaves `RUNNABLE`.

---

## Further reading (not spoken)

- [AWS Batch: Job states — STARTING and RUNNING](https://docs.aws.amazon.com/batch/latest/userguide/job_states.html) — what happens before your code runs
- [Amazon ECR: Image pull performance](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-pull-ecr-image.html) — large image pulls on fresh hosts
- [AWS: Lambda cold starts (contrast)](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtime-environment.html) — same idea, smaller footprint than GPU EC2
