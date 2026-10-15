# Video 001 — AWS Batch Job Lifecycle: Submitted to Succeeded

**Section:** 006 — Running the End-to-End GPU Pipeline
**Lecture#:** 001
**Sheet title:** AWS Batch Job Lifecycle: Submitted to Succeeded
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 006-001-aws-batch-job-lifecycle--submi

---

When a Batch job feels slow, the first question is not "is Python slow?" The first question is: what state is the job in right now?

That is how operators think in a company. They do not treat every delay as the same problem. They let the lifecycle narrow the diagnosis.

`SUBMITTED` means the request was accepted. `PENDING` is early handoff work. `RUNNABLE` means the job is eligible, but still waiting for a place to run. `STARTING` means capacity has been found and the container is being prepared. `RUNNING` means your workload is finally executing. Then the terminal state is either `SUCCEEDED` or `FAILED`.

Each state answers a different question.

If the job is stuck in `RUNNABLE`, your application has not started yet. Think capacity, quotas, or resource fit. If the job reaches `RUNNING` and then fails, now the application and logs matter. If it says `SUCCEEDED` but the expected output is missing, the problem may be in the workload behavior or the selected input, not in the scheduler.

This is why job states matter so much in GPU systems. GPU jobs can spend meaningful time before your code even begins, because the platform may still be finding capacity, pulling a large image, or warming the environment.

So do not just watch for success or failure. Watch how the job moves.

Next, we look at how one reusable job can process many different vendor folders without redefining everything each time.

---

## Further reading (not spoken)

- [AWS Batch: Job states](https://docs.aws.amazon.com/batch/latest/userguide/job_states.html) — SUBMITTED through SUCCEEDED/FAILED
- [AWS Batch: Troubleshooting](https://docs.aws.amazon.com/batch/latest/userguide/troubleshooting.html) — reading status reasons
- [CloudWatch Logs: Using log groups](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html) — where container stdout lands
