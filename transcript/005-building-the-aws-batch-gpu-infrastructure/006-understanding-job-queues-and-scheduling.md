# Video 006 — Understanding Job Queues and Scheduling

**Section:** 005 — Building the AWS Batch GPU Infrastructure
**Lecture#:** 006
**Sheet title:** Understanding Job Queues and Scheduling
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 005-006-understanding-job-queues-and-s

---

Compute environments define the machines. Job queues hold the waiting work. We do not submit a caption job directly to a GPU. We submit it to a queue, and that queue is connected to one or more ordered compute environments.

A queue is enabled or disabled, and it has an order for its compute environments. Batch takes `RUNNABLE` jobs and tries to place them on capacity from those environments in order. KodeFood uses `gpu-teaching-gpu-smoke-queue-spot` as the default path. A separate queue, `gpu-teaching-gpu-smoke-queue-on-demand`, is the fallback when Spot will not place.

Queue priority matters when several queues share capacity. Higher-priority queues receive scheduling preference. Our teaching path is simpler: one queue and one environment, with jobs waiting their turn for the single `g4dn.xlarge` allowed by the environment's maximum vCPUs.

Separate Spot and on-demand queues make the selected capacity path explicit. The lesson scripts point to the Spot queue by default. We switch the queue only when we deliberately choose on-demand and have confirmed that its quota can launch the instance.

For this small workload, ask one scheduling question: is the queue enabled, connected to a matching compute environment with room, and able to receive an instance from EC2? If any part is no, the job waits.

The queue holds work until capacity can take it. Next, we inspect the GPU job definition: image, memory, GPU count, environment variables, role, and logging.

---

## Further reading (not spoken)

- [AWS Batch: Job queues](https://docs.aws.amazon.com/batch/latest/userguide/job_queues.html) — queue state, priority, CE order
- [AWS Batch: Fair-share scheduling](https://docs.aws.amazon.com/batch/latest/userguide/fair-share-scheduling.html) — when multiple consumers share a queue
- [AWS Batch: Spot vs on-demand](https://docs.aws.amazon.com/batch/latest/userguide/spot_fleet_IAM_role.html) — capacity types behind queues
