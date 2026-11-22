# 08 — Submit the GPU job

This job’s only purpose is to print the GPU. When the log shows a T4, the Spot environment, the queue, and the job definition agree with each other.

## Submit

1. Stay in **Tokyo**.
2. **AWS Batch** → **Jobs** → **Submit new job**.
3. Name: **`kodefood-gpu-smoke-1`**
4. Job definition: **`kodefood-gpu-job`**
5. Job queue: **`kodefood-gpu-queue`**
6. Do not change vCPU, memory, or GPU in the overrides.
7. Submit.

## Watch it

The status path is the same as the CPU job: **SUBMITTED** → **RUNNABLE** → **STARTING** → **RUNNING** → **SUCCEEDED**.

RUNNABLE lasts longer here. Batch has to find a Spot `g4dn.xlarge`. A long RUNNABLE with no log stream means capacity has not been placed yet. It does not mean `nvidia-smi` failed.

When status is **SUCCEEDED**, open the log stream. You should see the `nvidia-smi` table and a GPU name that includes **Tesla T4**.

## If it never leaves RUNNABLE

1. Confirm the queue is `kodefood-gpu-queue`, not `kodefood-queue`. The CPU queue cannot place a GPU job.
2. Confirm the job definition GPU count is 1 and memory is 1024, not 16384.
3. Confirm the environment AMI is the NVIDIA ECS image, not the plain ECS image.
4. Wait and retry. Spot capacity in Tokyo comes and goes. Submitting the same recipe again is the right next move.
5. Do not switch this job to an on-demand GPU queue. If on-demand G and VT quota is 0, that queue also stays RUNNABLE.

## You are done when

`kodefood-gpu-smoke-1` is **SUCCEEDED** and the log shows a GPU.

Next: [09 — Clean up](../09-clean-up/GUIDE.md).
