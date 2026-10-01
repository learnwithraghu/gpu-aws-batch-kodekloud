# Video 001 — AWS Batch Job Lifecycle: Submitted to Succeeded

**Section:** 006 — Running the End-to-End GPU Pipeline
**Lecture#:** 001
**Sheet title:** AWS Batch Job Lifecycle: Submitted to Succeeded
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 006-001-aws-batch-job-lifecycle--submi

---

Once you submit, the job becomes a state machine. Learn the states and you stop treating every long wait as “the Python is slow.”

SUBMITTED means Batch accepted the request. PENDING is early bookkeeping — dependencies and internal handoff. RUNNABLE means the job is eligible to run but does not yet have a container on a machine. This is the state where capacity problems hide. No GPU instance yet means no application logs yet.

STARTING is the handoff onto an instance: agent placement, image pull beginning. RUNNING means the container is up and your command is executing — BLIP load, photo loop, CSV write. From RUNNING you end in SUCCEEDED or FAILED. Failed jobs still leave status reasons, exit codes, and often a log stream you can open.

Notice what each state is allowed to tell you. RUNNABLE forever is rarely a bug in `describe_items.py`. RUNNING with exit code one is where you open CloudWatch. SUCCEEDED without a CSV is an application or prefix mistake even though Batch is happy.

AWS documents this lifecycle the same way for CPU and GPU jobs. GPU only makes the RUNNABLE and STARTING stretches more expensive in wall-clock time because instances are scarcer and images are larger.

Map it once for KodeFood: submit caption job, watch RUNNABLE until Spot appears, STARTING while the multi-gigabyte image pulls, RUNNING while captions generate, SUCCEEDED when the catalog object exists.

That's it here for the lifecycle map: each state has a meaning, and RUNNABLE is not the same as running. Now the practical fork — how one job definition serves many vendor prefixes without registering a new revision every time.

---

## Further reading (not spoken)

- [AWS Batch: Job states](https://docs.aws.amazon.com/batch/latest/userguide/job_states.html) — SUBMITTED through SUCCEEDED/FAILED
- [AWS Batch: Troubleshooting](https://docs.aws.amazon.com/batch/latest/userguide/troubleshooting.html) — reading status reasons
- [CloudWatch Logs: Using log groups](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html) — where container stdout lands
