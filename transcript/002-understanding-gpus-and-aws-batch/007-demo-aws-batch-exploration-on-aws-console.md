# Demo 007 — AWS Batch exploration on AWS console
**Section:** 002 — Understanding GPUs and AWS Batch
**Lecture#:** 007
**Sheet title:** [Demo] AWS Batch exploration on AWS console
**Type:** Demo
**Runtime target:** ~8–10 minutes
**Topic code:** 002-007-[demo]-aws-batch-exploration-o

---

## Teaching goal

Give students a concrete visual tour of the four AWS Batch objects and the EC2 GPU Service Quotas in the AWS Management Console (`ap-northeast-1`) **before** we build containers or submit jobs in later sections.

By the end of the walkthrough, students can connect every concept from Section 002—compute environments, queues, job definition revisions, IAM roles, and G/VT quotas—to the exact fields in the console.

## Before you record

1. Sign in to the AWS Management Console and select region **Asia Pacific (Tokyo) `ap-northeast-1`**.
2. Open two browser tabs:
   - **AWS Batch** (`Compute environments`, `Job queues`, `Job definitions`, `Jobs`)
   - **Service Quotas** → **Amazon EC2**
3. Optional terminal window with read-only CLI commands from [`lessons/01-batch-and-gpu/README.md`](../../lessons/01-batch-and-gpu/README.md) if you want to show that the console and CLI report the exact same JSON fields.

Reference inventory: [`docs/aws-batch-setup.md`](../../docs/aws-batch-setup.md). Lesson notes: [`lessons/01-batch-and-gpu/README.md`](../../lessons/01-batch-and-gpu/README.md) and [`lessons/01-batch-and-gpu/theory.md`](../../lessons/01-batch-and-gpu/theory.md).

## Demo script (spoken flow)

1. **Confirm the region (`ap-northeast-1`).** Point out the region selector in the top bar. Remind viewers that Batch resources, ECR images, and Service Quotas are regional.
2. **Inspect Compute Environments (`Compute environments` in left nav).**
   - Point at `gpu-teaching-gpu-smoke-ce-spot` (and the fallback `gpu-teaching-gpu-smoke-ce-on-demand`). Note status `VALID` and state `ENABLED`.
   - Open `gpu-teaching-gpu-smoke-ce-spot` and highlight:
     - **Provisioning model:** `SPOT` (`SPOT_CAPACITY_OPTIMIZED`) vs `EC2` on the on-demand environment.
     - **Allowed instance types:** `g4dn.xlarge` (1 NVIDIA T4 GPU, 4 vCPU, 16 GiB RAM).
     - **vCPU limits:** `Minimum vCPUs = 0`, `Desired vCPUs = 0`, `Maximum vCPUs = 4`. Emphasize scale-to-zero—we pay nothing while the queue is empty.
     - **AMI type:** `ECS_AL2023_NVIDIA` (brings the NVIDIA driver + ECS agent).
     - **Instance role:** `ecsInstanceRole` (pulls the ECR image and writes CloudWatch logs, but cannot read S3).
3. **Inspect Job Queues (`Job queues` in left nav).**
   - Show `gpu-teaching-gpu-smoke-queue-spot` and `gpu-teaching-gpu-smoke-queue-on-demand`.
   - Click into `gpu-teaching-gpu-smoke-queue-spot` and show its **Compute environment order** linking directly to `gpu-teaching-gpu-smoke-ce-spot`.
   - Reinforce the mental model: *a queue holds waiting jobs, not running servers.*
4. **Inspect Job Definitions (`Job definitions` in left nav) — compare revisions.**
   - Select `gpu-teaching-caption-job` and show the revision history:
     - **Revision 1 (broken example):** Requests `16384` MiB memory on a 16 GiB `g4dn.xlarge`. Explain why this never places (`MISCONFIGURATION:JOB_RESOURCE_REQUIREMENT`) because the OS and ECS agent need a share of host memory.
     - **Revision 2 (incomplete example):** Lowered memory to `12288` MiB, but has no **Job role ARN** (`jobRoleArn`), so the container would fail on S3 `GetObject`/`PutObject`.
     - **Revision 4+ (working production recipe):** Requests `4` vCPUs, `12288` MiB memory, `1` GPU, sets `jobRoleArn` to `gpu-teaching-batch-job-role` for S3 access, and sends `awslogs` to `/aws/batch/job`.
5. **Inspect the Jobs view (`Jobs` in left nav).**
   - Filter by queue `gpu-teaching-gpu-smoke-queue-spot` and show the lifecycle columns (`SUBMITTED`, `RUNNABLE`, `STARTING`, `RUNNING`, `SUCCEEDED`, `FAILED`).
   - Remind viewers: *no CloudWatch log stream exists while a job is still in `RUNNABLE`.*
6. **Check EC2 GPU Service Quotas (switch to the Service Quotas tab).**
   - In **Service Quotas → Amazon EC2**, search for `G and VT`.
   - Highlight the two quotas that govern `g4dn.xlarge` (which needs 4 vCPUs per instance):
     - **All G and VT Spot Instance Requests** (`L-3819A6DF`) — e.g., `8` vCPUs in this teaching account.
     - **Running On-Demand G and VT instances** (`L-DB2E81BA`) — often `0` in new accounts until a quota increase is approved.
   - Show the **Request increase at account-level** button so students know where to ask for `4` or `8` vCPUs if their on-demand quota is `0`.

## What not to do in this demo

- Do not create, modify, or delete any compute environments, queues, or job definitions yet (that happens in Section 005).
- Do not submit a full captioning job yet (that happens in Section 006).

## Checkpoint for students

After this demo, students should be able to name the four Batch objects in the console, explain why revision `:1` (`16384` MiB) cannot place on `g4dn.xlarge`, distinguish `ecsInstanceRole` from `gpu-teaching-batch-job-role`, and check whether their account is allowed to launch Spot or On-Demand G/VT GPU instances.
