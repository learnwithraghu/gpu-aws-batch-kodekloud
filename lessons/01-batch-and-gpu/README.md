# Lesson 01 — AWS Batch and the GPU

This is the map for the rest of the course. You will create each piece in a later lesson. Here you learn what the pieces are, and what changes when the job needs a GPU.

Theory reading: [`theory.md`](theory.md).

Region for every command: `ap-northeast-1`.

## Four objects

| Object | What it is | Name in this course |
|--------|------------|---------------------|
| Compute environment | The machines Batch may start | `gpu-teaching-gpu-smoke-ce-spot` |
| Job queue | The line jobs wait in, attached to one environment | `gpu-teaching-gpu-smoke-queue-spot` |
| Job definition | The template: image, CPU, memory, GPU, role | `gpu-teaching-caption-job` |
| Job | One run of that template | one submission per vendor folder |

A queue does not hold servers. It holds jobs. The compute environment starts an instance when a job is waiting and can scale back to zero when the queue is empty (`minvCpus` is 0). You pay for the instance only while it is up.

## What “GPU in Batch” means

The instance type is `g4dn.xlarge`: one NVIDIA T4, 4 vCPU, 16 GiB of host memory.

Three settings have to agree, or the job never sees a GPU:

| Setting | Value | Why |
|---------|--------|-----|
| AMI | `ECS_AL2023_NVIDIA` | The ECS agent and the NVIDIA driver. A plain Amazon Linux AMI boots a GPU box whose container still has no CUDA device. |
| Job GPU | `1` | Batch places the job only on an instance that can give it one GPU. |
| Job memory | `12288` MiB | The host has 16 GiB. ECS keeps some for the OS and the agent. A job that asks for `16384` stays `RUNNABLE` forever with `MISCONFIGURATION:JOB_RESOURCE_REQUIREMENT`. |

The container also asks for 4 vCPU, which is the whole `g4dn.xlarge`. One GPU job, one instance.

## Two IAM roles

| Role | Who uses it | What it can do |
|------|-------------|----------------|
| `ecsInstanceRole` | The EC2 instance | Pull the image from ECR and write CloudWatch logs |
| `gpu-teaching-batch-job-role` | The container, via `jobRoleArn` | Read the images bucket and write the CSV |

The instance role cannot read S3. A job definition with no job role reaches the GPU and then fails on the first `GetObject`.

## Spot, and the fallback

The default environment buys Spot capacity (`SPOT_CAPACITY_OPTIMIZED`). Spot is cheaper and can be unavailable. The fallback is an on-demand environment and queue with the same instance type:

- `gpu-teaching-gpu-smoke-ce-on-demand`
- `gpu-teaching-gpu-smoke-queue-on-demand`

A job that sits in `RUNNABLE` for several minutes is almost always “no Spot capacity,” not a broken image. Lesson 08 switches the queue.

## The path one folder takes

```
laptop: docker build
    → ECR :latest
    → job definition (image + 1 GPU + 12288 MiB + job role)
    → submit one job for images/sample/
    → Batch starts a g4dn.xlarge
    → container runs python /app/describe_items.py
    → descriptions/sample/descriptions.csv
    → instance can go back to zero
```

## Look at the live account

These commands only read. Create nothing in this lesson.

```bash
export AWS_DEFAULT_REGION=ap-northeast-1

aws batch describe-compute-environments \
  --compute-environments gpu-teaching-gpu-smoke-ce-spot \
  --query 'computeEnvironments[0].{name:computeEnvironmentName,status:status,type:computeResources.type,instances:computeResources.instanceTypes,min:computeResources.minvCpus,max:computeResources.maxvCpus}'

aws batch describe-job-queues \
  --job-queues gpu-teaching-gpu-smoke-queue-spot \
  --query 'jobQueues[0].{name:jobQueueName,status:status,ce:computeEnvironmentOrder[0].computeEnvironment}'

aws batch describe-job-definitions \
  --job-definition-name gpu-teaching-caption-job \
  --status ACTIVE \
  --query 'sort_by(jobDefinitions, &revision)[-1].{revision:revision,req:containerProperties.resourceRequirements,role:containerProperties.jobRoleArn}'
```

Use the highest active revision. Revision `:1` asks for 16384 MiB. Revision `:2` has no job role. Revision `:3` and later are the ones that place and can write the CSV.

Names `gpu-teaching-ce`, `gpu-teaching-queue`, and `gpu-teaching-job-def` are not resources in this account. Do not create them.
