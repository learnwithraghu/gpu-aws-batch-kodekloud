# 09 — Clean up

Delete only the stack from this walkthrough. A compute environment with minimum vCPUs of 0 should already be empty, but a queue left ENABLED can launch machines the next time something is submitted.

Delete in this order. Batch will not delete a compute environment while a queue still points at it.

## Stop running work

1. Stay in **Tokyo**.
2. **AWS Batch** → **Jobs**. Pick **`kodefood-queue`** and **`kodefood-gpu-queue`** one at a time in the **Job queue** dropdown.
3. If any job is **SUBMITTED**, **PENDING**, or **RUNNABLE**, open it and **Cancel** it; if it is **STARTING** or **RUNNING**, **Terminate** it. Wait until no active jobs remain.

## Delete the queues

1. **AWS Batch** → **Job queues**.
2. Open **`kodefood-queue`** → **Actions** → **Disable**. Wait until **State** is **DISABLED**.
3. Choose **Actions** → **Delete**, then confirm **Delete job queue**.
4. Repeat for **`kodefood-gpu-queue`**.

## Delete the compute environments

1. **AWS Batch** → **Environments**.
2. Open **`kodefood-ce`** → **Actions** → **Disable**. Wait until **State** is **DISABLED**. This can take a minute or two.
3. Choose **Actions** → **Delete** and confirm deletion.
4. Repeat for **`kodefood-gpu-ce-spot`**.

## Job definitions

Job definitions have no hourly charge. You can leave `kodefood-job` and `kodefood-gpu-job` ACTIVE.

To retire one: **Job definitions** → open the job definition → select the active revision → **Actions** → **Deregister**. Deregister every revision you created.

## Leave these alone

Do not disable or delete anything named `gpu-teaching-*`, including:

- `gpu-teaching-gpu-smoke-ce-spot`
- `gpu-teaching-gpu-smoke-queue-spot`
- `gpu-teaching-gpu-smoke-queue-on-demand`
- `gpu-teaching-caption-job`
- `ecsInstanceRole`
- the VPC, subnet, and security group from step 01
- the log group `/aws/batch/job`

## You are done when

`kodefood-queue`, `kodefood-gpu-queue`, `kodefood-ce`, and `kodefood-gpu-ce-spot` are gone, and every `gpu-teaching-*` resource is still there.
