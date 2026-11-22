# 03 — Create the job queue

A job does not talk to the compute environment directly. You submit it to a queue. The queue is connected to the environment you just created.

## Create it

1. Stay in **Tokyo**.
2. **AWS Batch** → **Job queues** → **Create**.
3. Orchestration type: **Amazon Elastic Compute Cloud (Amazon EC2)**.
4. Name: **`kodefood-queue`**
5. Priority: **`1`**
6. Leave the scheduling policy empty.
7. Connected compute environment: **`kodefood-ce`**, order **`1`**.
8. State: **Enabled**.
9. Create the queue.

## Check it

Refresh until **Status** is **VALID** and **State** is **ENABLED**.

Open the queue and confirm the compute environment order lists `kodefood-ce` at order 1. If the environment is not in the list, the job will sit with nowhere to run.

## You are done when

`kodefood-queue` is VALID and points at `kodefood-ce`.

Next: [04 — Create the job definition](../04-create-the-job-definition/GUIDE.md).
