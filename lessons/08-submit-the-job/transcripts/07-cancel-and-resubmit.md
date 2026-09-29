# Video 07 — Cancel and resubmit
**Type:** Theory
**Runtime target:** ~3 minutes

---

So, what if the job is stuck and you need a clean redo? cancel-job tells Batch to stop a waiting job, with a reason string for the audit trail. In this course that job is usually still RUNNABLE on Spot. A waiting job has not started a container, so it has not written a CSV. Cancel does not undo S3 writes from a SUCCEEDED job. If the CSV is already at descriptions, stem, descriptions.csv, cancel leaves it. Cancel the stale id before you submit again. Leaving it in the queue is how two writers appear. The command takes a job id and a reason, not a queue name.

A second submit is not a harmless nudge. Picture your Spot queue. One job RUNNABLE for twenty minutes. Someone submits a duplicate on your on-demand queue. Spot capacity then appears. Both may run. You pay for two GPUs. Both write descriptions/sample/descriptions.csv when IMAGE_PREFIX is images/sample. The last writer wins.

Playbook: one active attempt per vendor folder. If RUNNABLE on Spot, wait, read statusReason, use helpers/watch_batch_job.sh. After about two minutes it prints desired vCPUs and the GPU quota. Do not add an on-demand job unless L-DB2E81BA is at least four, and unless you cancel the Spot attempt on purpose. Until that quota is at least four, on-demand never starts a container. Resubmit on Spot when capacity was the issue. Resubmit on-demand only after that check.

After a real fix, cancel the stale job, then submit once. A real fix might be quota approval, a corrected IMAGE_PREFIX, or a new image in ECR. The new submit still uses the job definition by name from your env file. Override stays python /app/describe_items.py with buckets, IMAGE_PREFIX, and BATCH_SIZE eight. Definition still asks for the GPU and memory from the lesson 07 revision. One KodeFood folder, one active attempt.

The demo is next. We submit one job and watch it.
