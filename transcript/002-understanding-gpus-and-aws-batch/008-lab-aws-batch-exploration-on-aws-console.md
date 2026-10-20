# Lab 008 — AWS Batch exploration on AWS console
**Section:** 002 — Understanding GPUs and AWS Batch
**Lecture#:** 008
**Sheet title:** [Lab] AWS Batch exploration on AWS console
**Type:** Lab
**Runtime target:** ~15–20 minutes
**Topic code:** 002-008-[lab]-aws-batch-exploration-on

---

## Lab goal

Explore the live AWS Batch GPU setup and EC2 Service Quotas in the AWS Console (and optionally via read-only AWS CLI commands) without creating or modifying any resources. You will verify how the compute environment, job queue, job definition revisions, IAM roles, and GPU quotas fit together.

## Prerequisites

- AWS Console access to the course environment in region **`ap-northeast-1` (Tokyo)**
- Optional: AWS CLI configured locally if you also want to run the read-only `describe-*` commands from [`lessons/01-batch-and-gpu/README.md`](../../lessons/01-batch-and-gpu/README.md)

## Steps

### 1. Inspect the GPU Compute Environments

1. Open the **AWS Batch** console and confirm the region in the top navigation bar is **Asia Pacific (Tokyo) `ap-northeast-1`**.
2. In the left navigation pane, choose **Compute environments**.
3. Locate `gpu-teaching-gpu-smoke-ce-spot` and `gpu-teaching-gpu-smoke-ce-on-demand`. Confirm both showStatus **`VALID`** and State **`ENABLED`**.
4. Click `gpu-teaching-gpu-smoke-ce-spot` and record:
   - **Provisioning model** (`SPOT` vs `EC2`)
   - **Instance types** (`g4dn.xlarge`)
   - **Minimum vCPUs**, **Desired vCPUs**, and **Maximum vCPUs** (`0` / `0` / `4`)
   - **AMI type** (`ECS_AL2023_NVIDIA`)
   - **Instance role** (`ecsInstanceRole`)

### 2. Trace the Job Queues to Compute Environments

1. In the left navigation pane, choose **Job queues**.
2. Open `gpu-teaching-gpu-smoke-queue-spot`.
3. Under **Compute environment order**, verify which compute environment is attached to this queue.
4. Repeat for `gpu-teaching-gpu-smoke-queue-on-demand`.

### 3. Compare Job Definition Revisions

1. In the left navigation pane, choose **Job definitions**.
2. Select `gpu-teaching-caption-job` and inspect its revisions:
   - Open **Revision 1** and check the requested **Memory** (`16384` MiB) and **Job role ARN**.
   - Open **Revision 2** and check what changed (`12288` MiB memory, still no `jobRoleArn`).
   - Open the latest active revision (**Revision 4+**) and confirm:
     - **vCPUs:** `4`
     - **Memory:** `12288` MiB
     - **GPUs:** `1`
     - **Job role ARN:** `gpu-teaching-batch-job-role`
     - **Log driver:** `awslogs` → `/aws/batch/job`

### 4. Check EC2 G and VT GPU Quotas

1. Open the **Service Quotas** console in `ap-northeast-1`.
2. Choose **AWS services** → **Amazon Elastic Compute Cloud (Amazon EC2)**.
3. Search for `G and VT` and note the **Applied quota value** for:
   - **All G and VT Spot Instance Requests** (`L-3819A6DF`)
   - **Running On-Demand G and VT instances** (`L-DB2E81BA`)

### 5. Optional: Run the Read-Only CLI Checks

If you have a terminal open, verify the same objects with the AWS CLI (create nothing):

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

aws service-quotas get-service-quota \
  --service-code ec2 --quota-code L-DB2E81BA --region ap-northeast-1 \
  --query 'Quota.{name:QuotaName,value:Value}'
```

## Deliverable

Answer these four questions based on what you observed in the console:

1. Why does `gpu-teaching-gpu-smoke-ce-spot` cost `$0` when no vendor jobs are running?
2. Why does `gpu-teaching-caption-job` revision `:1` (`16384` MiB) stay stuck in `RUNNABLE` on a `g4dn.xlarge` (`16` GiB host), while revision `:4` (`12288` MiB) can be placed?
3. Which IAM role pulls the container image from ECR, and which IAM role lets the Python script read and write S3 buckets?
4. What are the current vCPU values for `L-3819A6DF` (Spot G/VT) and `L-DB2E81BA` (On-Demand G/VT) in this region, and what happens if you submit a job to the on-demand queue when `L-DB2E81BA` is `0`?

## Common issues

| Symptom | Fix |
|---------|-----|
| Compute environments or queues list is empty | Check the top-right region selector in the console; switch to **Asia Pacific (Tokyo) `ap-northeast-1`** |
| Only the latest job definition revision appears | Change the **Status** filter or click into `gpu-teaching-caption-job` to view all revisions |
| Cannot find G and VT quotas | Ensure you are under **Service Quotas → Amazon EC2** (not AWS Batch) and search `G and VT` |
