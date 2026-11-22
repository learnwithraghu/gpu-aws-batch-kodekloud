# 08 — Submit the GPU job

This job’s only purpose is to print the GPU. When the log shows a T4, the Spot environment, the queue, and the job definition agree with each other.

## Submit

1. Stay in **Tokyo**.
2. **AWS Batch** → **Jobs** → **Submit new job**.
3. On page 1 (**General configuration**):
   - **Name**: **`kodefood-gpu-smoke-1`**
   - **Job definition**: **`kodefood-gpu-job`** (latest revision)
   - **Job queue**: **`kodefood-gpu-queue`**
   - Leave **Job dependencies**, **Array size**, and **Tags** empty, then choose **Next page**.
4. On page 2 (**Job overrides** and **Container overrides**), do not change vCPU, memory, or GPU, then choose **Next page**.
5. On the review page, choose **Submit**.

## Watch it

Open **Jobs** and pick **`kodefood-gpu-queue`** in the **Job queue** dropdown. The status path is the same as the CPU job: **SUBMITTED** → **PENDING** → **RUNNABLE** → **STARTING** → **RUNNING** → **SUCCEEDED**.

RUNNABLE lasts longer here. Batch has to find a Spot `g4dn.xlarge`. A long RUNNABLE with no log stream means capacity has not been placed yet. It does not mean `nvidia-smi` failed.

When status is **SUCCEEDED**, open **`kodefood-gpu-smoke-1`** and open **Log stream name** in **Details**. You should see the `nvidia-smi` table and a GPU name that includes **Tesla T4**.

## If it never leaves RUNNABLE

1. Confirm the queue is `kodefood-gpu-queue`, not `kodefood-queue`. The CPU queue cannot place a GPU job.
2. Confirm the job definition GPU count is 1 and memory is 1024, not 16384.
3. Confirm the environment AMI is **Amazon Linux 2023 (GPU)** (`ECS_AL2023_NVIDIA`), not the plain ECS image.
4. Wait and retry. Spot capacity in Tokyo comes and goes. Submitting the same recipe again is the right next move.
5. Do not switch this job to an on-demand GPU queue. If on-demand G and VT quota is 0, that queue also stays RUNNABLE.

## You are done when

`kodefood-gpu-smoke-1` is **SUCCEEDED** and the log shows a GPU.

Next: [09 — Clean up](../09-clean-up/GUIDE.md).
