# 06 — Create a GPU Spot environment

The menu photos need a GPU. This environment is a separate pool: Spot `g4dn.xlarge` machines, empty until a GPU job arrives. Keep the CPU environment from step 02. Do not edit it into a GPU environment.

## Create it

1. Stay in **Tokyo**.
2. **AWS Batch** → **Compute environments** → **Create**.
3. Type: **Amazon EC2**. Orchestration: **Managed**.
4. Name: **`kodefood-gpu-ce-spot`**
5. Service role: **`AWSServiceRoleForBatch`**
6. Instance role: **`ecsInstanceRole`**

## Capacity

1. Purchasing option: **Spot**.
2. Allocation strategy: **`SPOT_CAPACITY_OPTIMIZED`** if the form asks.
3. Allowed instance types: **`g4dn.xlarge`** only. That machine has one NVIDIA T4, 4 vCPUs, and 16 GiB of memory.
4. Minimum vCPUs: **`0`**
5. Desired vCPUs: **`0`**
6. Maximum vCPUs: **`4`**
7. AMI / image type: **Amazon Linux 2023, ECS-optimized, with NVIDIA GPU drivers**. The API name is `ECS_AL2023_NVIDIA`. The plain ECS AMI has no GPU driver, so a later `nvidia-smi` job cannot see the card.

## Network

Same as the CPU environment:

- VPC **`vpc-3f0b1a58`**
- Subnet **`subnet-b560b3fd`**
- Security group **`sg-bd00e4f5`**
- Assign a public IP if the form offers it

## Finish

Create it and wait until **Status** is **VALID** and **State** is **ENABLED**.

## Do not

- Do not set minimum vCPUs above 0. An idle GPU box keeps billing.
- Do not build an on-demand GPU environment in this step. On-demand G and VT quota in this account is often 0, so those jobs stay RUNNABLE forever.
- Do not modify `gpu-teaching-gpu-smoke-ce-spot` or any other `gpu-teaching-*` resource.

## You are done when

`kodefood-gpu-ce-spot` is VALID, uses Spot, uses `g4dn.xlarge`, uses the NVIDIA ECS AMI, and has minimum vCPUs of 0.

Next: [07 — Create the GPU queue and job](../07-create-the-gpu-queue-and-job/GUIDE.md).
