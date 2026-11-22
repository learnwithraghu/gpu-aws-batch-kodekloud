# 02 — Create the compute environment

The compute environment is the pool of machines. This first one is a small CPU pool so the later hello-world job has somewhere to land. The GPU pool is step 06.

## Create it

1. Stay in **Tokyo**.
2. **AWS Batch** → **Environments** (or **Compute environments**) → **Create** → **Compute environment**.
3. Compute environment type: **Amazon Elastic Compute Cloud (Amazon EC2)**. Not Fargate. Not ECS Managed Instances.
4. Orchestration: **Managed**.
5. Name: **`kodefood-ce`**
6. Service role: **`AWSServiceRoleForBatch`**.
7. Instance role: **`ecsInstanceRole`**. If it is missing, choose **Create a new instance profile**.

## Instance size

1. Purchasing option: **On-Demand**. Leave Spot off for this environment.
2. Allowed instance types: **`c6a.large`**. If that type is not offered, use **`c5.large`**. Do not leave this as “all types”.
3. Allocation strategy: **`BEST_FIT_PROGRESSIVE`** if the form asks.
4. Minimum vCPUs: **`0`**
5. Desired vCPUs: **`0`**
6. Maximum vCPUs: **`2`**
7. AMI / image type: **Amazon Linux 2023, ECS-optimized**. The API name is `ECS_AL2023`. Do not pick the NVIDIA image here.

Minimum `0` means the pool is empty until a job arrives. You are not billed for an idle machine.

## Network

1. VPC: **`vpc-3f0b1a58`**
2. Subnet: **`subnet-b560b3fd`**
3. Security group: **`sg-bd00e4f5`**
4. If you see **Assign public IP**, turn it **on**. The machine has to reach ECS and pull the public image.

## Finish

1. Create the environment.
2. Refresh until **Status** is **VALID** and **State** is **ENABLED**.

If status is **INVALID**, open **Status reason**. It is usually the subnet, the security group, the instance role, or the service role.

## You are done when

`kodefood-ce` is VALID and ENABLED, minimum vCPUs is 0, and the instance type is the small CPU type you chose.

Next: [03 — Create the job queue](../03-create-the-job-queue/GUIDE.md).
