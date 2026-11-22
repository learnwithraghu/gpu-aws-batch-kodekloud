# 05 — Submit the first job

Submit one job and watch it move. The interesting moment is the wait before the container starts.

## Submit

1. Stay in **Tokyo**.
2. **AWS Batch** → **Jobs** → **Submit new job**.
3. Name: **`kodefood-hello-1`**
4. Job definition: **`kodefood-job`**, latest revision.
5. Job queue: **`kodefood-queue`**
6. Leave container overrides empty.
7. Submit.

## Watch the status

Refresh the job. The normal path is:

1. **SUBMITTED** — Batch accepted it.
2. **RUNNABLE** — it is waiting for a machine. With minimum vCPUs at 0 this can last a few minutes. There are no application logs yet, because no container exists yet.
3. **STARTING** — the instance is registering with ECS.
4. **RUNNING** — the echo command is running.
5. **SUCCEEDED** — it finished.

Open the job, then open **Log stream name**. CloudWatch should show:

```text
KodeFood menu desk is connected
```

On the compute environment, desired vCPUs rises while the job runs and falls back toward 0 after it finishes.

## If it stays RUNNABLE

Check these in order:

1. `kodefood-ce` is still **VALID** and **ENABLED**.
2. `kodefood-queue` lists that environment.
3. The job asks for 1 vCPU and 512 MiB, which fits `c6a.large`.
4. The subnet has a route to the internet, or the wizard assigned a public IP. A private subnet with no NAT cannot pull the image.
5. The security group allows outbound traffic.

A job that never leaves RUNNABLE has no log stream. That is a placement problem, not a bug in the echo command.

## You are done when

`kodefood-hello-1` is **SUCCEEDED** and the log line is visible.

Next: [06 — Create a GPU Spot environment](../06-create-a-gpu-spot-environment/GUIDE.md).
