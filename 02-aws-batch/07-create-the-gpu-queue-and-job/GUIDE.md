# 07 — Create the GPU queue and job

The GPU machines need their own queue, and the recipe has to ask for a GPU. A job that does not ask for a GPU will not land on this environment in a useful way, and a job that asks for too much memory will never leave RUNNABLE.

## Queue

1. Stay in **Tokyo**.
2. **AWS Batch** → **Job queues** → **Create**.
3. **Orchestration type**: **Amazon Elastic Compute Cloud (Amazon EC2)**.
4. **Name**: **`kodefood-gpu-queue`**
5. **Priority**: **`1`**
6. Leave **Scheduling policy Amazon Resource Name (ARN)** empty.
7. **Connected compute environments**: select **`kodefood-gpu-ce-spot`** and confirm **Compute environment order** puts it at order **`1`**.
8. Leave **Job state time limit** (if shown) empty and keep state **Enabled** (default).
9. Choose **Create job queue** and wait until **Status** is **VALID**.

## Job definition

### Step 1: General configuration

1. **AWS Batch** → **Job definitions** → **Create**.
2. **Orchestration type**: **Amazon Elastic Compute Cloud (Amazon EC2)**.
3. **EC2 platform configuration**: turn **Enable multi-node parallel** **off**.
4. **Name**: **`kodefood-gpu-job`**
5. **Job attempts**: **`1`**; leave **Execution timeout**, **Scheduling priority**, **Retry strategy conditions**, **Tags**, and **Propagate tags** untouched, then choose **Next page**.

### Step 2: Container configuration and Environment configuration

Under **Container configuration**:

1. **Image**: **`nvidia/cuda:12.6.3-runtime-ubuntu22.04`**
2. **Command** (enter as a JSON string array):
   ```json
   ["nvidia-smi"]
   ```
3. Leave **Execution role**, **Job Role configuration**, and **Parameters** empty. `nvidia-smi` does not call AWS.

Under **Environment configuration**:

4. **vCPUs**: **`1`**
5. **Memory**: **`1024`** (MiB)
6. **Number of GPUs**: **`1`**
7. Leave **Environment variables** and **Secrets** empty, then choose **Next page**.

### Step 3: Linux, Filesystem, Task properties, and Logging configuration

1. Leave **Linux configuration**, **Filesystem configuration**, and **Task properties** at their defaults.
2. Under **Logging configuration**, keep **Log driver** as **`awslogs`** (default).
3. Under **Options**, choose **Add option** for each pair:
   - `awslogs-group` = `/aws/batch/job`
   - `awslogs-region` = `ap-northeast-1`
   - `awslogs-stream-prefix` = `kodefood-gpu`
4. Leave **Secrets** empty, then choose **Next page**.

### Step 4: Job definition review

Review the configuration and choose **Create job definition**.

## Check the recipe before you submit

Open `kodefood-gpu-job` and confirm all of these:

| Field | Value |
|-------|--------|
| Image | `nvidia/cuda:12.6.3-runtime-ubuntu22.04` |
| vCPUs | 1 |
| Memory | 1024 MiB |
| GPUs | 1 |

`g4dn.xlarge` has 16 GiB, but ECS does not hand the container the whole machine. A job that asks for **16384** MiB never places. Keep this smoke job at **1024**.

## You are done when

`kodefood-gpu-queue` is VALID and connected to `kodefood-gpu-ce-spot`, and `kodefood-gpu-job` requests exactly 1 GPU.

Next: [08 — Submit the GPU job](../08-submit-the-gpu-job/GUIDE.md).
