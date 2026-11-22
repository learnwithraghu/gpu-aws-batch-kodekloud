# 03 — Create the job queue

A job does not talk to the compute environment directly. You submit it to a queue. The queue is connected to the environment you just created.

## Create it

1. Stay in **Tokyo**.
2. **AWS Batch** → **Job queues** → **Create**.
3. **Orchestration type**: **Amazon Elastic Compute Cloud (Amazon EC2)**.
4. **Name**: **`kodefood-queue`**
5. **Priority**: **`1`**
6. Leave **Scheduling policy Amazon Resource Name (ARN)** empty.
7. **Connected compute environments**: select **`kodefood-ce`** (it must already be **VALID**) and use **Compute environment order** to keep `kodefood-ce` at order **`1`**.
8. Leave **Job state time limit** (if shown) empty and keep the queue state **Enabled** (default).
9. Choose **Create job queue**.

## Check it

Refresh until **Status** is **VALID** and **State** is **ENABLED**.

Open the queue and confirm the compute environment order lists `kodefood-ce` at order 1. If the environment is not in the list, the job will sit with nowhere to run.

## You are done when

`kodefood-queue` is VALID and points at `kodefood-ce`.

Next: [04 — Create the job definition](../04-create-the-job-definition/GUIDE.md).
