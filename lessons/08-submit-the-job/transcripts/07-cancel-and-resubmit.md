# Video 07 — Cancel and resubmit
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

cancel-job tells Batch to stop a job that is still waiting, and you pass a reason string so the audit trail says why. The command is aws batch cancel-job, then the job id, then the reason. In this course that job is usually still RUNNABLE, waiting on Spot capacity. A waiting job has not started a container, so it has not written a CSV. Cancel does not undo S3 writes from a job that already reached SUCCEEDED. If the CSV is already at descriptions, then the folder stem, then descriptions.csv, cancel leaves that object where it is. You cancel the stale id before you submit again. Leaving it in the queue is how two writers appear. The command takes that job id and a reason. It does not take a queue name, so you are stopping one id, not every job on the Spot queue.

Discipline matters because a second submit is not a harmless nudge. Picture the Spot queue, gpu-teaching-gpu-smoke-queue-spot, in ap-northeast-1. One job has been RUNNABLE for twenty minutes. Someone submits a duplicate on the on-demand queue, gpu-teaching-gpu-smoke-queue-on-demand, to help. Spot capacity then appears. Both jobs may run. You pay for two GPUs. Both write the same key, descriptions/sample/descriptions.csv, when IMAGE_PREFIX is images/sample. The last writer wins, and the debugging gets worse, not better.

The playbook for this course is one active attempt per vendor folder. If the job is RUNNABLE on Spot, wait, read statusReason, and use helpers/watch_batch_job.sh. That helper, after about two minutes, prints the compute environment's desired vCPU count and the GPU quota. Do not add an on-demand job unless the on-demand quota L-DB2E81BA is at least four, and unless you cancel the Spot attempt on purpose. Until that quota is at least four, on-demand never starts a container. Resubmit on Spot when capacity was the issue. Resubmit on the on-demand queue only after that quota check. The reason string in the cancel call can say there was no Spot capacity and you are resubmitting on demand, but only when that quota actually allows it.

After a real fix, cancel the stale job, then submit once. A real fix might be the quota approval, a corrected IMAGE_PREFIX, or a new image pushed to ECR. The new submit still uses the job definition name gpu-teaching-caption-job, so Batch picks the highest active revision. You do not pin revision one or revision two. The override is still python /app/describe_items.py, with the bucket variables, IMAGE_PREFIX, and BATCH_SIZE eight. The definition still asks for one GPU and twelve thousand two hundred eighty-eight mebibytes. This course does not want two folders' worth of parallelism on the same stem. One folder, one active attempt.

On the screen, two job ids converge on one S3 key and that picture is marked wrong. A single job id pointing at the same key is marked right.

The demo is next. We submit one job and watch it.
