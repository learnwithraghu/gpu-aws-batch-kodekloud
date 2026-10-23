# Demo 006 — Job definition and dummy job

**Section:** 003 — AWS Batch: Scaling GPU Workloads  
**Type:** Demo (AWS Console)  
**Creates / uses:** `kk-batch-demo-job` on `kk-batch-demo-queue-cpu`

## Goal

Register a **dummy** job definition (the recipe), submit one job, and watch **SUBMITTED → RUNNABLE → RUNNING → SUCCEEDED** with CloudWatch logs. Proves the control plane from demo 004 before any GPU work.

## Prerequisites

- [004 — Batch control plane](004-create-the-batch-control-plane.md) complete (CE + queue VALID)
- Log group `/aws/batch/job` exists

---

## Part A — Job definition

1. **AWS Batch** → **Job definitions** → **Create**.
2. Orchestration: **ECS**
3. Name: **`kk-batch-demo-job`**
4. Attempts: **1**
5. Container:
   - **Image:** `public.ecr.aws/amazonlinux/amazonlinux:2023` (or `busybox:latest`)
   - **Command:** echo `kk-batch-demo` `CPU` `job` `succeeded` (separate args if the UI uses an arg list)
   - **vCPUs:** `1`
   - **Memory:** `512` or `1024` MiB
   - **GPUs:** none / `0`
6. Job role: not required for this echo job (no S3).
7. Logging: `awslogs` → `/aws/batch/job`, region `ap-northeast-1`.
8. **Create** (revision 1 ACTIVE).

**Checkpoint A:** Definition shows public image, 0 GPUs, echo command.

---

## Part B — Submit and watch

1. **Jobs** → **Submit new job** (or from the job definition → Submit).
2. Job name: **`kk-batch-demo-run-1`**
3. Definition: **`kk-batch-demo-job`** (latest)
4. Queue: **`kk-batch-demo-queue-cpu`**
5. No overrides → **Submit**.
6. Refresh status:
   - **RUNNABLE** — waiting for capacity (normal on a cold CE with min 0; **no app logs yet**)
   - **STARTING / RUNNING** — instance up
   - **SUCCEEDED** — done
7. Open CloudWatch → `/aws/batch/job` → newest stream. Confirm the echo line.

**Checkpoint B:** Job succeeded; logs show the demo string; CE can scale desired vCPUs back toward 0.

---

## If it stays RUNNABLE

- CE still VALID?
- vCPU/memory fit `c6a.large` and CE max?
- Subnet/SG allow pulling the public image?

## What not to do

- Do not use `gpu-teaching-caption-job` or the private ECR image here.
- Do not request GPUs or 16384 MiB.
- When finished with the CPU path, clean up `kk-batch-demo-*` ([README](README.md)) — do not delete `gpu-teaching-*`.

## Next

Continue Section 003 videos (scheduling through Spot/monitoring), then [015 — Run a GPU job on Spot](015-run-a-gpu-job-on-spot.md).
