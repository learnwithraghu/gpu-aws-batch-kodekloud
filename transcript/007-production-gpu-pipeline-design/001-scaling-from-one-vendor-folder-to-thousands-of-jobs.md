# Video 001 — Scaling from One Vendor Folder to Thousands of Jobs

**Section:** 007 — Production GPU Pipeline Design
**Lecture#:** 001
**Sheet title:** Scaling from One Vendor Folder to Thousands of Jobs
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 007-001-scaling-from-one-vendor-folde

---

You captioned one stem — `images/sample` in, one CSV out. KodeFood does not ship one vendor. Onboarding, menu refreshes, and re-checks mean hundreds or thousands of folders. The question is not “can the model handle more photos?” It is “how do you turn one proven job into many units of work without reinventing Batch?”

Two patterns dominate. First: many submits. A small orchestrator — Lambda, Step Functions, or a script — lists vendor stems and calls `submit-job` once per stem, each with its own `IMAGE_PREFIX` override. Same job definition, same image, different folder. Failures stay isolated: vendor A’s AccessDenied does not kill vendor B.

Second: array jobs. AWS Batch can submit one parent that expands into many child indices. You map index to stem — from a list in S3, or from a naming convention — and each child still runs the same container. Arrays shine when the work units are uniform and you want one submit API call plus shared retry policy. Many independent submits shine when stems arrive continuously and you want per-vendor priority or different queues.

Either way, keep the unit of work the same: one folder, one CSV. Do not smash thousands of photos into one container “to save cold starts.” That creates long-running monsters and worse Spot interruption pain. Uber’s Michelangelo writing biases toward small, restartable tasks — similar advice to what we are applying here, at a very different scale. Further reading has that article if you want their production framing.

Thousands of jobs also amplify RUNNABLE waits, logs, and quotas — so track queue depth and define re-submit rules for poison stems.

Scale is mostly submission shape, not a new model. Next: what happens when those jobs compete — parallelism, queues, and whether the GPU is actually busy.

---

## Further reading (not spoken)

- [AWS Batch: Array jobs](https://docs.aws.amazon.com/batch/latest/userguide/array_jobs.html) — parent submit that expands into indexed children
- [AWS Batch: Submitting a job](https://docs.aws.amazon.com/batch/latest/userguide/submit_job.html) — overrides and parameters per unit of work
- [Uber Engineering: Michelangelo](https://www.uber.com/blog/michelangelo-machine-learning-platform/) — production ML job granularity at scale
