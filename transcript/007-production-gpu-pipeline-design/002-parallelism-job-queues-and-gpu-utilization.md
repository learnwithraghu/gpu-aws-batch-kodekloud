# Video 002 — Parallelism, Job Queues and GPU Utilization

**Section:** 007 — Production GPU Pipeline Design
**Lecture#:** 002
**Sheet title:** Parallelism, Job Queues and GPU Utilization
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 007-002-parallelism-job-queues-and-

---

Submitting a thousand jobs does not create a thousand GPUs. Batch parallelism is bounded by three numbers: RUNNABLE jobs, instances the compute environment may launch, and GPUs on those instances. Our `g4dn.xlarge` has one GPU, and the job definition requests one GPU per container. That gives us one running job per instance. Throughput is therefore limited by placement, Spot supply, quota, and `maxvCpus`.

Queues express operating intent. Queue priority decides which work receives capacity first. Fair-share scheduling prevents one workload from consuming a shared compute environment. KodeFood could use a high-priority on-demand queue for menu launches and a Spot queue for overnight backfills. The job definition stays the same; urgency changes.

Utilization tells us whether that capacity was useful. A GPU waiting for photos to download is billed but idle. Micro-batching helps keep the device active after the model loads, while cold starts reduce useful time. Measure GPU activity and memory through tools such as NVIDIA DCGM; a SUCCEEDED status alone cannot show wasted capacity.

Watch for three common causes during an incident: CPU-only preparation running on GPU instances, a memory request that prevents placement, and `maxvCpus` set below the intended concurrency.

Parallelism helps only when the queue admits work and the GPU stays busy. Next we decide when that operating model belongs on Batch and when another service is a better fit.

---

## Further reading (not spoken)

- [AWS Batch: Job queues](https://docs.aws.amazon.com/batch/latest/userguide/job_queues.html) — priorities and scheduling across compute environments
- [AWS Batch: Fair-share scheduling](https://docs.aws.amazon.com/batch/latest/userguide/fairsharequeue.html) — sharing limited capacity across users or workloads
- [NVIDIA DCGM](https://developer.nvidia.com/dcgm) — GPU health and utilization metrics used in production fleets
