# Video 04 — Stuck in RUNNABLE
**Type:** Theory
**Runtime target:** ~3 minutes

---

Here's the thing. RUNNABLE means Batch knows about the job and has not placed it on a started task yet. It does not mean Python is slow. describe_items.py is not running. The model is not loading. The folder is not being listed.

Students open /aws/batch/job, see nothing, and edit the caption program. No container means no stdout. Logs appear only after STARTING or RUNNING. Empty logs while RUNNABLE are expected.

Five checks cover the usual causes. First, Spot capacity is dry. Job on your Spot queue, long RUNNABLE, statusReason talks about capacity. Desired vCPUs may stay at zero or climb slowly. That is common here. Second, on-demand G and VT quota is zero. Code L-DB2E81BA. On your on-demand queue, zero means Batch never launches a g4dn even when the environment looks healthy. Third, memory cannot place. Sixteen thousand three hundred eighty-four mebibytes on g4dn.xlarge shows MISCONFIGURATION:JOB_RESOURCE_REQUIREMENT. Working request is the GPU and memory from the lesson 07 revision. Fourth, compute environment INVALID or disabled, or queue bound to the wrong environment. Fifth, job and environment in different regions. Rare, and catastrophic.

Habit: aws batch describe-jobs with the job id. Read statusReason. Read logStreamName. While RUNNABLE that stream is often null. Submit the job definition by name so Batch uses the highest active revision from lesson 07—broken revisions never place or lack S3 and logs.

Stay on Spot. helpers/watch_batch_job.sh polls every fifteen seconds and prints statusReason. After about two minutes of RUNNABLE it says no container has started, so this is not describe_items.py. It prints compute environment desired vCPUs and the GPU quota. Desired at zero means the environment has not asked EC2 for a machine yet. Fix placement first. Do not rebuild from an empty log group. KodeFood's menu never sees a CSV while the job is still waiting for capacity.

Quotas, and why the first run is slow after placement, are next.
