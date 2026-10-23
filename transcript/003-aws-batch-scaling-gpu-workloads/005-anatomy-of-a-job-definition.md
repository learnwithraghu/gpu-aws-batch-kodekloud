# Video 005 — Anatomy of a Job Definition

**Section:** 003 — AWS Batch: Scaling GPU Workloads
**Lecture#:** 005
**Sheet title:** Anatomy of a Job Definition
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 003-005-anatomy-of-a-job-definition

---

The queue can hold work, and the compute environment can offer machines. What still has to be explicit is the recipe.

That recipe is the job definition. It turns a vague idea — “run the caption container” — into an execution contract Batch can place.

Why does that contract matter so much in a company?

Because production failures often come from silent assumptions. Which image should run? How much CPU and memory does the task need? Which identity may the container use to read images and write the CSV? Should failed attempts retry? Where do logs go?

A job definition answers those questions up front. It is not just packaging. It is the stable agreement between the application team and the platform about how a run is allowed to look.

Teams also treat revisions carefully. Each registration creates a snapshot of that contract. Change the image, the memory request, or the job role, and you are not editing a comment. You are changing placement behavior, permissions, or runtime stability for future submissions.

So the useful mindset is this: keep stable execution details in the job definition, and leave only run-specific inputs — which vendor folder, which batch size — for overrides at submit time.

With a clear recipe in place, the next console demo registers that definition and launches a simple dummy job. After that, we slow down and ask how Batch actually chooses when and where a waiting job may start.

---

## Further reading (not spoken)

- [AWS Batch: Job definitions](https://docs.aws.amazon.com/batch/latest/userguide/job_definitions.html) — image, resources, roles, retries, logging
- [AWS Batch: Resource requirements](https://docs.aws.amazon.com/batch/latest/userguide/job_definitions.html#containerproperties.resourceRequirements) — vCPU, memory, and GPU fields
- [Amazon ECS: Task IAM roles](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html) — container identity separate from the instance role
