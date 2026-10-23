# Demo 015 — Run a GPU job on Spot

**Section:** 003 — AWS Batch: Scaling GPU Workloads  
**Type:** Demo (AWS Console)  
**Uses:** live `gpu-teaching-gpu-smoke-*` (inspect + submit — do not recreate)

## Goal

One GPU/Spot console pass: inspect the live **GPU Spot compute environment**, submit a **`nvidia-smi` smoke job**, and frame Spot capacity, interruptions, and the on-demand fallback queue.

## Prerequisites

- Region **Tokyo (`ap-northeast-1`)**
- Videos through GPU AMIs / Spot cost / monitoring recommended
- Job definition **`gpu-teaching-gpu-smoke-job`** ACTIVE (CUDA image, 1 GPU, ~1024 MiB, `nvidia-smi` command)
- Log group `/aws/batch/job`

---

## Part A — Inspect the GPU Spot CE

1. **Batch** → **Compute environments** → **`gpu-teaching-gpu-smoke-ce-spot`**.
2. Call out:

| Field | Expected |
|-------|----------|
| State / Status | ENABLED / VALID |
| Purchase | **Spot** (capacity optimized) |
| Instance | **`g4dn.xlarge`** |
| Min / Max vCPUs | **0** / **4** |
| AMI | **ECS AL2023 NVIDIA** |
| Instance role | **`ecsInstanceRole`** |
| Network | `subnet-b560b3fd` / `sg-bd00e4f5` |

3. Open queue **`gpu-teaching-gpu-smoke-queue-spot`** — CE order **1**.
4. Optional contrast: on-demand CE/queue with the same GPU shape (fallback only).

**Checkpoint A:** Students can say *Spot + g4dn + NVIDIA ECS AMI + min zero*.

---

## Part B — Submit the GPU smoke job

1. **Job definitions** → **`gpu-teaching-gpu-smoke-job`** — confirm **GPU = 1** and a CUDA/nvidia image.  
   Lab account only: create that definition if missing. Do **not** edit `gpu-teaching-caption-job` here.
2. **Submit job:**
   - Name: `kk-gpu-spot-1`
   - Definition: `gpu-teaching-gpu-smoke-job`
   - Queue: **`gpu-teaching-gpu-smoke-queue-spot`**
3. Narrate states: **RUNNABLE** (placement / Spot capacity — no logs) → **RUNNING** → **SUCCEEDED**.
4. CloudWatch `/aws/batch/job`: show the `nvidia-smi` table (T4) and success line.

**Checkpoint B:** SUCCEEDED with a visible GPU in logs.

---

## Part C — Spot economics and fallback

1. Why Spot for KodeFood-style work: finite, restartable, scale to zero.
2. **RUNNABLE** on Spot often means capacity, not broken Python.
3. Interruption: design for reclaim (small units, durable S3 outputs, retries).
4. Open **`gpu-teaching-gpu-smoke-queue-on-demand`**. Same shape, different purchase.  
   If Service Quotas **Running On-Demand G and VT** is **0**, on-demand also stays RUNNABLE — switching queues does not invent quota.
5. Leave live `gpu-teaching-*` in place. Clean up only `kk-batch-demo-*` from demos 004/006.

**Checkpoint C:** Spot is default; RUNNABLE is placement; on-demand needs quota; interruptions are operational, not a reason to avoid Spot.

---

## If it stays RUNNABLE

- Spot capacity thin → wait/retry.
- On-demand quota 0 → do not expect fallback to place.
- Wrong memory/GPU on a different job def (e.g. caption at 16384 MiB) → misconfiguration.

## What not to do

- Do not delete or disable the live Spot CE.
- Do not run the full KodeFood caption job here (later lessons: ECR image, job role, 12288 MiB).
- Do not recreate `gpu-teaching-*` resources in the shared teaching account.

## After this section

Section 004 — Building the GPU Application (`photos.py` / `describe_items.py`).
