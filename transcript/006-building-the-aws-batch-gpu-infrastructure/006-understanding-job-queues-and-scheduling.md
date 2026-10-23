# Video 006 — Understanding Job Queues and Scheduling

**Section:** 006 — Building the AWS Batch GPU Infrastructure
**Lecture#:** 006
**Sheet title:** Understanding Job Queues and Scheduling
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 006-006-understanding-job-queues-and-s

---

If compute environments describe possible machines, job queues describe waiting work.

This is where the scheduling mindset becomes clearer.

You do not hand a job directly to a GPU. You hand it to a queue, and the queue becomes the place where Batch decides what should run first and where it should try to run it.

That sounds simple, but it reflects a real company need. Work often arrives faster than capacity. There has to be some orderly place where jobs wait, compete for resources, and follow the team’s scheduling policy instead of pure chance.

So a queue is not just a holding area. It is part of the control plane. It expresses intent about how work should flow toward capacity.

This becomes especially important with GPU systems because GPUs are scarce and expensive. Teams often care about which workloads get first access, which capacity path they prefer, and what fallback logic should exist when the cheaper path does not place.

So when you think about queues, think beyond "list of waiting jobs." Think scheduling policy.

Next, we look at the job definition, which describes what Batch should actually run once the scheduler finds capacity.

---

## Further reading (not spoken)

- [AWS Batch: Job queues](https://docs.aws.amazon.com/batch/latest/userguide/job_queues.html) — queue state, priority, CE order
- [AWS Batch: Fair-share scheduling](https://docs.aws.amazon.com/batch/latest/userguide/fair-share-scheduling.html) — when multiple consumers share a queue
- [AWS Batch: Spot vs on-demand](https://docs.aws.amazon.com/batch/latest/userguide/spot_fleet_IAM_role.html) — capacity types behind queues
