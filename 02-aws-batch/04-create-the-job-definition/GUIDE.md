# 04 — Create the job definition

The job definition is the recipe: which image, which command, and how much CPU and memory. This recipe only prints a line. It proves the queue and the environment before any GPU work.

## Step 1: General configuration

1. Stay in **Tokyo**.
2. **AWS Batch** → **Job definitions** → **Create**.
3. **Orchestration type**: **Amazon Elastic Compute Cloud (Amazon EC2)**.
4. **EC2 platform configuration**: turn **Enable multi-node parallel** **off**.
5. **Name**: **`kodefood-job`**
6. Leave **Execution timeout** empty and keep **Scheduling priority** off.
7. **Job attempts**: **`1`**. Retrying a hello-world job hides a bad setup.
8. Leave **Retry strategy conditions**, **Tags**, and **Propagate tags** untouched, then choose **Next page**.

## Step 2: Container configuration and Environment configuration

Under **Container configuration**:

1. **Image**: **`public.ecr.aws/amazonlinux/amazonlinux:2023`**
2. **Command** (enter as a JSON string array):
   ```json
   ["echo", "KodeFood menu desk is connected"]
   ```
3. Leave **Execution role**, **Job Role configuration**, and **Parameters** empty. This container does not call AWS APIs.

Under **Environment configuration**:

4. **vCPUs**: **`1`**
5. **Memory**: **`512`** (MiB)
6. **Number of GPUs**: leave empty or **`0`**
7. Leave **Environment variables** and **Secrets** empty, then choose **Next page**.

## Step 3: Linux, Filesystem, Task properties, and Logging configuration

1. Leave **Linux configuration**, **Filesystem configuration**, and **Task properties** at their defaults.
2. Under **Logging configuration**, keep **Log driver** set to **`awslogs`** (default).
3. Under **Options**, choose **Add option** for each of these three pairs:
   - `awslogs-group` = `/aws/batch/job`
   - `awslogs-region` = `ap-northeast-1`
   - `awslogs-stream-prefix` = `kodefood`
4. Leave **Secrets** empty, then choose **Next page**.

## Step 4: Job definition review

Review the settings and choose **Create job definition**. Open **`kodefood-job`** and confirm:

- Platform is EC2
- Image is `public.ecr.aws/amazonlinux/amazonlinux:2023`
- vCPU is 1, memory is 512 MiB, GPU is 0
- Revision **1** is **ACTIVE**

## You are done when

`kodefood-job` revision 1 is ACTIVE and does not request a GPU.

Next: [05 — Submit the first job](../05-submit-the-first-job/GUIDE.md).
