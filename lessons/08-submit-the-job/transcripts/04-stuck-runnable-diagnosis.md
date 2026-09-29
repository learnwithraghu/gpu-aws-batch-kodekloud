# Video 04 — Stuck in RUNNABLE
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

RUNNABLE means Batch knows about the job and could run it, but has not placed it on a started task yet. It does not mean Python is slow. describe_items.py is not running. The model is not loading. The folder of photos is not being listed.

Students misdiagnose this because they open the log group /aws/batch/job, see nothing, and edit the caption program. No container means no standard output. Logs appear only after the job reaches STARTING or RUNNING. While it sits in RUNNABLE, an empty log group is expected. It is not a logging bug, and it is not a bug in the Python.

Five checks cover the usual causes. First, Spot capacity is dry. The job is on gpu-teaching-gpu-smoke-queue-spot, in ap-northeast-1, RUNNABLE for a long time, and statusReason talks about capacity. The compute environment's desired vCPU count may stay at zero or climb slowly. That is the common case in this course. Second, the on-demand G and VT quota is zero. The code is L-DB2E81BA, Running On-Demand G and VT instances. On the queue gpu-teaching-gpu-smoke-queue-on-demand, a value of zero means Batch never launches a g4dn, even when the compute environment looks healthy. Third, the memory request cannot place. Sixteen thousand three hundred eighty-four mebibytes on a g4dn.xlarge shows up as the status reason MISCONFIGURATION:JOB_RESOURCE_REQUIREMENT, and the job never reaches RUNNING. The working request is twelve thousand two hundred eighty-eight mebibytes, plus one GPU. Fourth, the compute environment is INVALID or disabled, or the queue is bound to the wrong environment. The describe calls come back INVALID or disabled. Fifth, the job and the environment are in different regions or accounts. A job in Tokyo and a compute environment in Oregon will not meet. It is rare, and it is catastrophic.

The habit is aws batch describe-jobs, with the job id. Read statusReason. Read the container log stream name. While the job is RUNNABLE that stream name is often null. You submit gpu-teaching-caption-job by name so Batch uses the highest active revision, not revision one or revision two. Revision one is the broken sixteen-thousand-mebibyte definition. A wrong revision can leave you in this state even when Spot capacity exists.

In this course, stay on the Spot queue. The watch helper, helpers/watch_batch_job.sh, polls every fifteen seconds and prints statusReason on each line. After about two minutes of RUNNABLE it says no container has started, so this is not describe_items.py. It then prints the compute environment status, state, desired vCPUs, and max vCPUs, and it prints the GPU service quota. A desired count that stays at zero means the environment has not asked EC2 for the machine yet. You fix placement first. You do not rebuild the image from an empty log group.

On the screen, one job sits in RUNNABLE with a badge that says no log stream yet, and a decision tree branches to those five checks.

Quotas, and why the first run is slow after placement, are next.
