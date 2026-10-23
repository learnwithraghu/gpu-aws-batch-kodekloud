# Demo 004 — Create the Batch control plane

**Section:** 003 — AWS Batch: Scaling GPU Workloads  
**Type:** Demo (AWS Console)  
**Creates:** `kk-batch-demo-lt`, `kk-batch-demo-ce-cpu`, `kk-batch-demo-queue-cpu`

## Goal

In one console pass, build the three pieces Batch needs before any recipe exists: a **launch template** (host defaults), a **CPU compute environment** (the kitchen), and a **job queue** (the ticket line). No GPU yet.

## Prerequisites

- Region **Tokyo (`ap-northeast-1`)**
- Instance profile **`ecsInstanceRole`**
- Network: VPC `vpc-3f0b1a58`, subnet `subnet-b560b3fd`, SG `sg-bd00e4f5`

---

## Part A — Launch template

1. **EC2** → **Launch Templates** → **Create launch template**.
2. Name: **`kk-batch-demo-lt`**
3. Description: `Section 003 CPU demo for Batch`
4. **AMI:** Amazon Linux 2023 (x86_64). Batch will also use ECS-optimized images via the CE; the template still needs a valid AMI.
5. **Instance type:** optional here; CE will pin `c6a.large`.
6. **Key pair:** optional (jobs do not need SSH).
7. **Network:** enable auto-assign public IP; security group **`sg-bd00e4f5`**. Prefer leaving subnet unset so Batch supplies it from the CE.
8. **Advanced details → IAM instance profile:** **`ecsInstanceRole`**
9. **Create launch template.**

**Checkpoint A:** Template `kk-batch-demo-lt` exists with `ecsInstanceRole` and `sg-bd00e4f5`.

---

## Part B — Compute environment (CPU)

1. **AWS Batch** → **Compute environments** → **Create**.
2. Name: **`kk-batch-demo-ce-cpu`**
3. Orchestration: **ECS**
4. Provisioning: **On-Demand**
5. Instance types: **`c6a.large`**
6. Min vCPUs **0**, Max vCPUs **2**
7. Launch template: **`kk-batch-demo-lt`** (default / version 1)
8. Image type: **ECS-optimized Amazon Linux 2023** (`ECS_AL2023`) — **not** NVIDIA
9. Network: VPC / subnet / SG from prerequisites
10. Instance role: **`ecsInstanceRole`**
11. **Create.** Wait until **VALID** / **ENABLED**.

If **INVALID**, read **Status reason** (subnet, SG, instance profile, or service role).

**Checkpoint B:** `kk-batch-demo-ce-cpu` is VALID; min 0; no idle instances while the queue is empty.

---

## Part C — Job queue

1. **AWS Batch** → **Job queues** → **Create**.
2. Name: **`kk-batch-demo-queue-cpu`**
3. Priority: **1**
4. Connected CE: **`kk-batch-demo-ce-cpu`** (order 1)
5. State: **Enabled** → **Create.** Wait until **VALID**.

**Checkpoint C:** Queue lists `kk-batch-demo-ce-cpu` as order 1.

---

## What not to do

- Do not create or rename live `gpu-teaching-*` resources.
- Do not set Minimum vCPUs above 0.
- Do not use Fargate for this path (we are training the EC2 + launch-template model used later for GPUs).
- Do not submit a job yet — that is demo 006.

## Next

Video: Anatomy of a Job Definition → then [006 — Job definition and dummy job](006-job-definition-and-dummy-job.md).
