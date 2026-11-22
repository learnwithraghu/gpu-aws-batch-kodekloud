# 04 — Create the job definition

The job definition is the recipe: which image, which command, and how much CPU and memory. This recipe only prints a line. It proves the queue and the environment before any GPU work.

## Create it

1. Stay in **Tokyo**.
2. **AWS Batch** → **Job definitions** → **Create**.
3. Orchestration type: **Amazon Elastic Compute Cloud (Amazon EC2)**.
4. Name: **`kodefood-job`**
5. Execution timeout: leave empty.
6. Job attempts: **1** if the form asks. Retrying a hello-world job hides a bad setup.

## Container

1. Image: **`public.ecr.aws/amazonlinux/amazonlinux:2023`**
2. Command:
   - One text box: `echo KodeFood menu desk is connected`
   - Separate argument boxes: first box `echo`, second box `KodeFood menu desk is connected`
3. vCPUs: **`1`**
4. Memory: **`512`**
5. Number of GPUs: leave empty or **`0`**
6. Job role: leave empty. This container does not call AWS APIs.
7. Do not add environment variables.

## Logging

1. Log driver: **`awslogs`**
2. Options:
   - `awslogs-group` = `/aws/batch/job`
   - `awslogs-region` = `ap-northeast-1`
   - `awslogs-stream-prefix` = `kodefood`
3. If the form has a single logging section, point it at the log group `/aws/batch/job` in Tokyo.

## Finish

Create the job definition. Open it and confirm:

- Platform is EC2
- Image is the public Amazon Linux image
- vCPU is 1, memory is 512, GPU is 0
- Revision **1** is **ACTIVE**

## You are done when

`kodefood-job` revision 1 is ACTIVE and does not request a GPU.

Next: [05 — Submit the first job](../05-submit-the-first-job/GUIDE.md).
