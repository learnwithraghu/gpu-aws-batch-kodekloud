# 06 — Create a GPU Spot environment

The menu photos need a GPU. This environment is a separate pool: Spot `g4dn.xlarge` machines, empty until a GPU job arrives. Keep the CPU environment from step 02. Do not edit it into a GPU environment.

## Open the wizard

1. Stay in **Tokyo**.
2. **AWS Batch** → **Environments** → **Create environment** → **Compute environment**.

## Step 1: Compute environment configuration

1. **Compute environment configuration**: **Amazon Elastic Compute Cloud (Amazon EC2)**.
2. **Orchestration type**: **Managed**.
3. **Name**: **`kodefood-gpu-ce-spot`**
4. **Service role**: **`AWSServiceRoleForBatch`**
5. **Instance role**: **`ecsInstanceRole`**
6. Leave **Tags** and **EC2 tags** empty, then choose **Next**.

## Step 2: Instance configuration

1. **Use EC2 Spot instances** → toggle **Enable using Spot instances** **on**.
2. **Maximum % on-demand price**: leave empty (defaults to `100`% — you still pay the current Spot market price, never above On-Demand).
3. **Spot fleet role**: with **`SPOT_CAPACITY_OPTIMIZED`** or **`SPOT_PRICE_CAPACITY_OPTIMIZED`**, the Batch API does not require a Spot Fleet role (it is only required for legacy `BEST_FIT`). If the console still asks for one, select an existing role that uses the **`AmazonEC2SpotFleetTaggingRole`** managed policy (or create one under **IAM** → **Roles** → **Create role** → **AWS service** → **EC2** → **EC2 - Spot Fleet Tagging**).
4. **Minimum vCPUs**: **`0`**
5. **Desired vCPUs**: **`0`**
6. **Maximum vCPUs**: **`4`** (change this from the default **`256`** — `g4dn.xlarge` has 4 vCPUs, capping the pool at one GPU instance).
7. **Scale down delay (minutes)** *(optional)*: leave empty / default.
8. **Allowed instance types**: clear the default (`optimal` or `default_x86_64`) and choose **`g4dn.xlarge`** only. That machine has one NVIDIA T4, 4 vCPUs, and 16 GiB of memory.
9. **Allocation strategy**: **`SPOT_CAPACITY_OPTIMIZED`** (or **`SPOT_PRICE_CAPACITY_OPTIMIZED`**).
10. Expand **Additional configuration** → **EC2 configuration** → **Image type**: choose **Amazon Linux 2023 (GPU)** (API name `ECS_AL2023_NVIDIA`). Leave **Image ID override**, **Placement group**, **EC2 key pair**, and **Launch templates** untouched. The plain non-GPU AMI lacks NVIDIA drivers, so a later `nvidia-smi` job cannot see the GPU.
11. Choose **Next**.

## Step 3: Network configuration

1. **Virtual Private Cloud (VPC) ID**: **`vpc-3f0b1a58`**
2. **Subnets**: clear all other pre-selected subnets and keep only **`subnet-b560b3fd`**. There is no public-IP toggle here; the subnet's auto-assign public IPv4 setting provides the public IP.
3. **Security groups**: **`sg-bd00e4f5`**
4. Choose **Next** (or **Next page**). If **Container insights** appears, leave it disabled.

## Step 4: Review

Review the settings, choose **Create compute environment**, and on **Environments** wait until **Status** is **VALID** and **State** is **ENABLED**.

## Do not

- Do not set minimum vCPUs above 0. An idle GPU box keeps billing.
- Do not build an on-demand GPU environment in this step. On-demand G and VT quota in this account is often 0, so those jobs stay RUNNABLE forever.
- Do not modify `gpu-teaching-gpu-smoke-ce-spot` or any other `gpu-teaching-*` resource.

## You are done when

`kodefood-gpu-ce-spot` is VALID, uses Spot, uses `g4dn.xlarge`, uses the Amazon Linux 2023 (GPU) AMI, and has minimum vCPUs of 0.

Next: [07 — Create the GPU queue and job](../07-create-the-gpu-queue-and-job/GUIDE.md).
