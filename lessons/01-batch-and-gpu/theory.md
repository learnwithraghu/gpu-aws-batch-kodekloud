# Lesson 01 — Theory

This lesson is the map. The CLI labs later create the pieces you read about here.

## What AWS Batch is for

AWS Batch runs container jobs on a managed pool of EC2 instances (via ECS). You submit work; Batch places it when capacity exists.

It is not a notebook host and not an interactive shell. You do not SSH into a GPU box to type Python. You define a job once, then submit many runs of that job. This course’s work — one folder of photos in, one CSV out — fits that pattern.

## The four objects

| Object | Role |
|--------|------|
| Compute environment | Which machines Batch may start (instance type, Spot or on-demand, network) |
| Job queue | The line jobs wait in; bound to one or more compute environments |
| Job definition | The template: image, CPU, memory, GPU, IAM role, default command |
| Job | One run of that template |

The definition is the recipe. The job is one cook of that recipe for one vendor folder. The queue holds waiting cooks. The compute environment is the kitchen that can appear and disappear.

## Scale-to-zero

Course compute environments set `minvCpus` to 0. When the queue is empty, Batch does not keep a `g4dn` running.

You pay for the instance while a job needs it. When the catalog CSV is written and no other job is waiting, desired capacity can return to zero. That matches sparse vendor drops from lesson 00.

## GPU placement requirements

A GPU job only runs if three things agree:

1. **AMI** — `ECS_AL2023_NVIDIA` (or equivalent) so the host has NVIDIA drivers and the ECS agent. A plain Amazon Linux AMI can boot a GPU-shaped instance whose container still has no CUDA device.
2. **Job GPU** — `GPU=1` so Batch places the job only where one GPU is available.
3. **Memory under usable host RAM** — a `g4dn.xlarge` has 16 GiB. ECS keeps some for the OS and agent. Asking for `16384` MiB yields `MISCONFIGURATION:JOB_RESOURCE_REQUIREMENT` and the job never leaves `RUNNABLE`. This course uses **12288** MiB.

## `g4dn` / T4 in practice

`g4dn.xlarge` gives one NVIDIA T4, 4 vCPU, and 16 GiB of host memory. That is enough for a small caption model and groups of about 8 photos.

This course asks for the whole machine (4 vCPU, 1 GPU). One catalog job, one instance. You are not packing several GPU jobs onto one box.

## Instance role vs job role

Two IAM identities matter:

| Role | Who assumes it | Typical powers |
|------|----------------|----------------|
| Instance profile (`ecsInstanceRole`) | The EC2 host | Pull the image from ECR, write CloudWatch logs |
| Job role (`jobRoleArn`) | The container task | Read the images bucket, write the CSV bucket |

The instance role does not get S3 for this course. A job that reaches the GPU without a job role fails on the first `GetObject`. Lesson 07 wires both.

## Spot vs on-demand for GPU jobs

Spot capacity is cheaper and can disappear or be unavailable. On-demand is steadier and costs more.

The default queue in this course is Spot. A job that sits in `RUNNABLE` for a long time on Spot is often “no Spot GPU right now,” not a broken image.

**On-demand is not automatic.** EC2 Service Quotas control how many G/VT instance vCPUs you may run:

| Quota | Code | Role in this course |
|-------|------|---------------------|
| Running On-Demand G and VT instances | `L-DB2E81BA` | Must be **≥ 4** before a `g4dn.xlarge` on-demand job can start |
| All G and VT Spot Instance Requests | `L-3819A6DF` | Spot path; this teaching account uses **8** |

Many new accounts default **on-demand G/VT to 0**. With quota 0, the on-demand CE and queue can look `VALID` and `Healthy`, yet every job stays `RUNNABLE` forever: no instance, no container, no CloudWatch logs. That is an account limit, not a Batch misconfiguration.

### How to check

```bash
aws service-quotas get-service-quota \
  --service-code ec2 --quota-code L-DB2E81BA --region ap-northeast-1 \
  --query 'Quota.{name:QuotaName,value:Value}'
```

`helpers/watch_batch_job.sh` prints the same quota when a job stays `RUNNABLE` for about two minutes.

### How to request an increase

1. AWS Console → **Service Quotas** → **Amazon EC2** → region **ap-northeast-1**.
2. Open **Running On-Demand G and VT instances**.
3. **Request increase** to at least **4** (this course often asks for **8** so one `g4dn.xlarge` fits with headroom).
4. Wait until the case is **Approved** and `get-service-quota` shows the new value. Until then, stay on the Spot queue.

Only after on-demand G/VT ≥ 4 should you treat `gpu-teaching-gpu-smoke-queue-on-demand` as a real fallback. Lesson 08 covers cancel and resubmit once that is true.

## Why not Lambda / SageMaker here

**Lambda** has short timeouts, limited disk, and no simple “attach one T4 for a few minutes” path that matches this image size and model download.

**SageMaker** is strong for managed training and hosting endpoints. For a rare, folder-sized batch of photos, Batch’s “queue a container, start a GPU, stop” model is the smaller piece of machinery.

This course uses Batch because the workload is a containerized batch inference job with a clear start and end — not an always-on API.
