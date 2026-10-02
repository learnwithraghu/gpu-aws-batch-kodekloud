# Video 001 — Scaling from One Vendor Folder to Thousands of Jobs

**Section:** 007 — Production GPU Pipeline Design
**Lecture#:** 001
**Sheet title:** Scaling from One Vendor Folder to Thousands of Jobs
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 007-001-scaling-from-one-vendor-folde

---

We have proved one unit of work: `images/sample` goes in and one CSV comes out. Production adds vendor onboarding, menu refreshes, and rechecks, so that unit repeats hundreds or thousands of times. In design review, the question is not whether BLIP can see more photos. It is how we scale submission while keeping each failure contained.

There are two practical patterns. The first is independent submissions. A small orchestrator—Lambda, Step Functions, or a script—lists vendor stems and calls `submit-job` once per stem, with a separate `IMAGE_PREFIX` override. The image and job definition stay fixed. An AccessDenied for vendor A does not stop vendor B.

The second pattern is an array job. One parent expands into indexed children. Each index maps to a stem from an S3 manifest or a naming convention, and each child runs the same container. Arrays fit a known, uniform batch with a shared retry policy. Independent submissions fit continuous arrivals, per-vendor priority, or routing to different queues.

Keep the recovery boundary at one folder and one CSV. Combining thousands of photos in one container may save a few cold starts, but it creates a long-running job with a large retry cost when Spot interrupts it. The same small, restartable-task principle appears in systems such as Uber’s Michelangelo.

At this scale, queue depth, quota pressure, and log volume become incident signals. Define a retry ceiling and a quarantine path for a poison stem before the first large backfill.

The model has not changed; the submission and recovery design has. Next we review how those jobs compete for GPUs and whether the devices are doing useful work.

---

## Further reading (not spoken)

- [AWS Batch: Array jobs](https://docs.aws.amazon.com/batch/latest/userguide/array_jobs.html) — parent submit that expands into indexed children
- [AWS Batch: Submitting a job](https://docs.aws.amazon.com/batch/latest/userguide/submit_job.html) — overrides and parameters per unit of work
- [Uber Engineering: Michelangelo](https://www.uber.com/blog/michelangelo-machine-learning-platform/) — production ML job granularity at scale
