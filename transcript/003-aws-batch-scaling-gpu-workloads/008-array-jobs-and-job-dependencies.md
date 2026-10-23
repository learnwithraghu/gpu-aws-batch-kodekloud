# Video 008 — Array Jobs and Job Dependencies

**Section:** 003 — AWS Batch: Scaling GPU Workloads
**Lecture#:** 008
**Sheet title:** Array Jobs and Job Dependencies
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 003-008-array-jobs-and-job-dependencie

---

One vendor folder is a useful teaching job. Production is rarely one folder.

When hundreds of vendors upload menus in the same hour, nobody wants to click submit hundreds of times. Teams need a way to fan out the same recipe across many independent units of work.

That is what array jobs give you. One submission creates many child jobs that share a job definition. Each child gets an index, and your container uses that index to pick which folder or shard to process. The scheduler still places each child on its own timeline as capacity appears.

Why does that matter operationally? Because failure stays local. If vendor forty-two fails, vendor forty-three can still succeed. You retry the bad unit, not the entire marketplace backlog.

Job dependencies solve a different shape. Sometimes captioning must finish before a second step aggregates results, or a validation job must pass before a publish job runs. Dependencies let Batch wait for N to finish before starting M, without a human watching the console.

Uber’s platform writing leans on the same idea: keep work units small and restartable, then compose them. Array jobs are horizontal fan-out. Dependencies are ordered composition.

For KodeFood, picture one array across vendor stems for captioning, then a dependent rollup only after the array succeeds. That is production thinking without building a custom orchestrator on day one.

Next, we make the GPU part of the recipe explicit — how a job definition asks for an accelerator, and why the memory number on that request can silently block placement.

---

## Further reading (not spoken)

- [AWS Batch: Array jobs](https://docs.aws.amazon.com/batch/latest/userguide/array_jobs.html) — fan-out with AWS_BATCH_JOB_ARRAY_INDEX
- [AWS Batch: Job dependencies](https://docs.aws.amazon.com/batch/latest/userguide/job_dependencies.html) — N_TO_N and sequential pipeline patterns
- [Uber Engineering: Michelangelo](https://www.uber.com/blog/michelangelo-machine-learning-platform/) — small, restartable ML work units
