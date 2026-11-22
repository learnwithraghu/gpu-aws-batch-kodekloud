# 02 — Create the compute environment

The compute environment is the pool of machines. This first one is a small CPU pool so the later hello-world job has somewhere to land. The GPU pool is step 06.

## Open the wizard

1. Stay in **Tokyo**.
2. **AWS Batch** → **Environments** → **Create environment** → **Compute environment**.

## Step 1: Compute environment configuration

1. **Compute environment configuration**: **Amazon Elastic Compute Cloud (Amazon EC2)** (not Fargate, not Amazon ECS Managed Instances, and not Amazon EKS).
2. **Orchestration type**: **Managed**.
3. **Name**: **`kodefood-ce`**
4. **Service role**: **`AWSServiceRoleForBatch`**
5. **Instance role**: **`ecsInstanceRole`**. If it is missing, choose **Create a new instance profile**.
6. Leave **Tags** and **EC2 tags** empty, then choose **Next**.

## Step 2: Instance configuration

1. **Use EC2 Spot instances** → **Enable using Spot instances**: leave **off** (that keeps it On-Demand; there is no separate On-Demand toggle).
2. **Minimum vCPUs**: **`0`**
3. **Desired vCPUs**: **`0`**
4. **Maximum vCPUs**: **`2`** (change this from the default **`256`**).
5. **Scale down delay (minutes)** *(optional)*: leave empty / default.
6. **Allowed instance types**: clear the default selection (`optimal` or `default_x86_64`) and choose **`c6a.large`**. If that type is not offered, use **`c5.large`**. Do not leave broad or all instance families selected.
7. **Allocation strategy**: **`BEST_FIT_PROGRESSIVE`** (recommended for EC2 On-Demand).
8. Expand **Additional configuration**:
   - Leave **Placement group** and **EC2 key pair** empty.
   - Under **EC2 configuration** → **Image type**: choose **Amazon Linux 2023** (API name `ECS_AL2023`, the default since January 2026; Amazon Linux 2 AMIs reached end-of-support on June 30, 2026). Leave **Image ID override** empty. Do not pick the GPU image here.
   - Leave **Launch templates** untouched.
9. Choose **Next**.

Minimum `0` means the pool is empty until a job arrives. You are not billed for an idle machine.

## Step 3: Network configuration

1. **Virtual Private Cloud (VPC) ID**: **`vpc-3f0b1a58`**
2. **Subnets**: clear all other pre-selected subnets (the console selects every subnet in the VPC by default) and keep only **`subnet-b560b3fd`**. There is no "Assign public IP" toggle here — instances receive a public IP from the subnet's auto-assign public IPv4 setting confirmed in step 01.
3. **Security groups**: **`sg-bd00e4f5`**
4. Choose **Next** (or **Next page**). If **Container insights** appears before review, leave it disabled to avoid extra CloudWatch charges.

## Step 4: Review

1. Review the settings and choose **Create compute environment**.
2. Back on **Environments**, refresh until **Status** is **VALID** and **State** is **ENABLED**.

If status is **INVALID**, open **Status reason**. It is usually the subnet, the security group, the instance role, or the service role.

## You are done when

`kodefood-ce` is VALID and ENABLED, minimum vCPUs is 0, and the instance type is the small CPU type you chose.

Next: [03 — Create the job queue](../03-create-the-job-queue/GUIDE.md).
