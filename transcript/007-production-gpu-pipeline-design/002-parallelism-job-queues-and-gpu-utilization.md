# Video 002 — Parallelism, Job Queues and GPU Utilization

**Section:** 007 — Production GPU Pipeline Design
**Lecture#:** 002
**Sheet title:** Parallelism, Job Queues and GPU Utilization
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 007-002-parallelism-job-queues-and-

---

You can submit a thousand jobs in a minute. That does not mean a thousand GPUs appear. Parallelism in Batch is negotiated between three things: how many jobs are RUNNABLE, how many instances the compute environment may launch, and how many GPUs those instances actually have. On our path, one `g4dn.xlarge` carries one GPU, and the job definition pins one GPU per container. So one running job per machine. Throughput equals how many machines Batch can place — subject to Spot, quota, and `maxvCpus`.

Queues are the control surface. Priority between queues decides who gets capacity first. Fair-share scheduling can stop one team from monopolizing a shared CE. For KodeFood you might run a high-priority on-demand queue for menu go-live deadlines and a Spot queue for overnight backfills. Same job definition, different urgency. That is parallelism with intent, not “fire everything at once.”

Utilization is the quiet metric. A GPU idle while photos download is paid for but unused. That is why micro-batching inside the job matters — keep the device busy once the model is loaded — and why cold starts hurt. NVIDIA’s DCGM guidance and production inference teams push the same idea: measure device activity and memory, not only “job succeeded.”

Anti-patterns to avoid: packing CPU-only prep onto GPU instances, memory so high the job never places, and `maxvCpus` so low that parallelism dies while Spot still has room.

That's it here for utilization thinking: parallel jobs only help if the GPU is busy with useful work and the queue is not fighting itself. That raises a sharper product question — when Batch is the right tool for that pattern, and when it is not.

---

## Further reading (not spoken)

- [AWS Batch: Job queues](https://docs.aws.amazon.com/batch/latest/userguide/job_queues.html) — priorities and scheduling across compute environments
- [AWS Batch: Fair-share scheduling](https://docs.aws.amazon.com/batch/latest/userguide/fairsharequeue.html) — sharing limited capacity across users or workloads
- [NVIDIA DCGM](https://developer.nvidia.com/dcgm) — GPU health and utilization metrics used in production fleets
