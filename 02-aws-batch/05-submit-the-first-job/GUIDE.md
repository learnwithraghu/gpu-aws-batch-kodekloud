# 05 — Submit the first job

Submit one job and watch it move. The interesting moment is the wait before the container starts.

## Submit

1. Stay in **Tokyo**.
2. **AWS Batch** → **Jobs** → **Submit new job**.
3. On page 1 (**General configuration**):
   - **Name**: **`kodefood-hello-1`**
   - **Job definition**: **`kodefood-job`** (latest revision)
   - **Job queue**: **`kodefood-queue`**
   - Leave **Job dependencies**, **Array size**, and **Tags** empty, then choose **Next page**.
4. On page 2 (**Job overrides** and **Container overrides**), leave all overrides and **Additional configuration** untouched, then choose **Next page**.
5. On the review page, choose **Submit**.

## Watch the status

Open **Jobs**, pick **`kodefood-queue`** in the **Job queue** dropdown (Batch displays one queue at a time), and refresh. The normal path is:

1. **SUBMITTED** — Batch accepted it.
2. **PENDING** — waiting on dependencies (skipped quickly when none are set).
3. **RUNNABLE** — it is waiting for a machine. With minimum vCPUs at 0 this can last a few minutes. There are no application logs yet, because no container exists yet.
4. **STARTING** — the instance is registering with ECS.
5. **RUNNING** — the echo command is running.
6. **SUCCEEDED** — it finished.

Open **`kodefood-hello-1`**, then in the **Details** pane open **Log stream name**. CloudWatch should show:

```text
KodeFood menu desk is connected
```

On the compute environment, desired vCPUs rises while the job runs and falls back toward 0 after it finishes.

## If it stays RUNNABLE

Check these in order:

1. `kodefood-ce` is still **VALID** and **ENABLED**.
2. `kodefood-queue` lists that environment.
3. The job asks for 1 vCPU and 512 MiB, which fits `c6a.large`.
4. The subnet (`subnet-b560b3fd`) has **Auto-assign public IPv4 address** enabled and a route to the internet. A private subnet with no NAT cannot pull the image.
5. The security group allows outbound traffic.

A job that never leaves RUNNABLE has no log stream. That is a placement problem, not a bug in the echo command.

## You are done when

`kodefood-hello-1` is **SUCCEEDED** and the log line is visible.

Next: [06 — Create a GPU Spot environment](../06-create-a-gpu-spot-environment/GUIDE.md).
