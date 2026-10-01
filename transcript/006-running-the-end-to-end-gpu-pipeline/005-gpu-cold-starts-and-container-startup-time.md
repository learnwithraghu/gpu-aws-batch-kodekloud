# Video 005 — GPU Cold Starts and Container Startup Time

**Section:** 006 — Running the End-to-End GPU Pipeline
**Lecture#:** 005
**Sheet title:** GPU Cold Starts and Container Startup Time
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 006-005-gpu-cold-starts-and-container-

---

You submit. The job is correct. Still minutes pass before the first log line from BLIP. That gap is cold start, and on GPU Batch it is usually several stacked waits — not one.

First the compute environment may be at zero. EC2 must launch a `g4dn.xlarge`, boot the NVIDIA ECS-optimized AMI, and register the ECS agent. That alone can take minutes when Spot has to find a pool.

Then the container image pulls from ECR. Our teaching image is multi-gigabyte: CUDA, PyTorch, transformers, application code. First pull on a fresh instance dominates. Later jobs on a warm host may reuse layers and feel faster.

Then the process starts and loads the model. BLIP weights move onto GPU memory. Only after that does photo iteration begin. If weights download from the network on first use, add another stretch.

Production inference platforms treat cold start as a first-class cost. AWS Lambda has documented cold starts for CPUs; GPU Batch cold starts are heavier because the machine and the image are both large. Some teams keep `minvCpus` above zero to hide AMI boot — they pay idle GPU time to buy latency. Our course keeps min at zero to protect the teaching bill, so you feel the full cold path.

Measure wall clock from submit to first RUNNING log, then from RUNNING to first caption. You will see infrastructure time and model time separately — and you will stop blaming `describe_items.py` for the AMI boot.

That's it here for cold starts: AMI boot, image pull, and model load are real time before the first caption. Sometimes the wait is worse — the job never leaves RUNNABLE. Next we unpack what capacity and quotas are doing while you wait.

---

## Further reading (not spoken)

- [AWS Batch: Job states — STARTING and RUNNING](https://docs.aws.amazon.com/batch/latest/userguide/job_states.html) — what happens before your code runs
- [Amazon ECR: Image pull performance](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-pull-ecr-image.html) — large image pulls on fresh hosts
- [AWS: Lambda cold starts (contrast)](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtime-environment.html) — same idea, smaller footprint than GPU EC2
