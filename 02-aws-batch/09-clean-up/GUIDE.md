# 09 — Clean up

Delete only the stack from this walkthrough. A compute environment with minimum vCPUs of 0 should already be empty, but a queue left ENABLED can launch machines the next time something is submitted.

Delete in this order. Batch will not delete a compute environment while a queue still points at it.

## Stop running work

1. Stay in **Tokyo**.
2. **Jobs**. Filter each of `kodefood-queue` and `kodefood-gpu-queue`.
3. If any job is **RUNNABLE**, **STARTING**, or **RUNNING**, open it and **Cancel** it. Wait until it is no longer running.

## Delete the queues

1. **Job queues**.
2. Select **`kodefood-queue`** → **Disable**. Wait until the state is **DISABLED**.
3. **Delete** it.
4. Repeat for **`kodefood-gpu-queue`**.

## Delete the compute environments

1. **Compute environments**.
2. Select **`kodefood-ce`** → **Disable**. Wait until it is **DISABLED**. This can take a minute or two.
3. **Delete** it.
4. Repeat for **`kodefood-gpu-ce-spot`**.

## Job definitions

Job definitions have no hourly charge. You can leave `kodefood-job` and `kodefood-gpu-job` ACTIVE.

To retire one: open the job definition → select the active revision → **Deregister**. Deregister every revision you created.

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
