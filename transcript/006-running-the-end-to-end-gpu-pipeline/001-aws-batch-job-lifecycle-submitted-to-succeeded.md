# Video 001 — AWS Batch Job Lifecycle: Submitted to Succeeded

**Section:** 006 — Running the End-to-End GPU Pipeline
**Lecture#:** 001
**Sheet title:** AWS Batch Job Lifecycle: Submitted to Succeeded
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 006-001-aws-batch-job-lifecycle--submi

---

After submission, the job moves through a state machine. Read the current state before deciding that Python is slow.

`SUBMITTED` means Batch accepted the request. `PENDING` covers early bookkeeping, dependencies, and internal handoff. `RUNNABLE` means the job is eligible, but no container has been placed on a machine. Capacity problems appear here. With no container, there are no application logs.

`STARTING` is the handoff to an instance: placement and image pull. `RUNNING` means the container is up and the command is executing: BLIP load, photo loop, and CSV write. The terminal state is `SUCCEEDED` or `FAILED`. A failed job still provides a status reason, an exit code, and often a log stream.

Let the state narrow the diagnosis. A job stuck in `RUNNABLE` has not started `describe_items.py`; check capacity, quotas, and resource fit. A `RUNNING` job that exits with code 1 is ready for CloudWatch inspection. A `SUCCEEDED` job without a CSV points to application behavior or the selected prefix, even though Batch considers the command successful.

The lifecycle is the same for CPU and GPU jobs. GPU jobs often spend longer in `RUNNABLE` and `STARTING` because instances are scarcer and images are larger.

For this lab, watch `RUNNABLE` while Batch seeks Spot capacity, `STARTING` while the multi-gigabyte image pulls, and `RUNNING` while captions are generated. Confirm both `SUCCEEDED` and the expected catalog object.

That state map is our first diagnostic tool. Next, we use one job definition for many vendor prefixes without registering a new revision for every run.

---

## Further reading (not spoken)

- [AWS Batch: Job states](https://docs.aws.amazon.com/batch/latest/userguide/job_states.html) — SUBMITTED through SUCCEEDED/FAILED
- [AWS Batch: Troubleshooting](https://docs.aws.amazon.com/batch/latest/userguide/troubleshooting.html) — reading status reasons
- [CloudWatch Logs: Using log groups](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html) — where container stdout lands
