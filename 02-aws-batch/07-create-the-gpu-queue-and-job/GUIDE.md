# 07 — Create the GPU queue and job

The GPU machines need their own queue, and the recipe has to ask for a GPU. A job that does not ask for a GPU will not land on this environment in a useful way, and a job that asks for too much memory will never leave RUNNABLE.

## Queue

1. Stay in **Tokyo**.
2. **AWS Batch** → **Job queues** → **Create**.
3. Orchestration type: **Amazon EC2**.
4. Name: **`kodefood-gpu-queue`**
5. Priority: **`1`**
6. Connected compute environment: **`kodefood-gpu-ce-spot`**, order **`1`**.
7. State: **Enabled**.
8. Create it and wait until it is **VALID**.

## Job definition

1. **Job definitions** → **Create**.
2. Orchestration type: **Amazon EC2**.
3. Name: **`kodefood-gpu-job`**
4. Image: **`nvidia/cuda:12.6.3-runtime-ubuntu22.04`**
5. Command:
   - One text box: `nvidia-smi`
   - Argument boxes: a single box, `nvidia-smi`
6. vCPUs: **`1`**
7. Memory: **`1024`**
8. Number of GPUs: **`1`**
9. Job role: leave empty. `nvidia-smi` does not call AWS.
10. Logging: `awslogs` to `/aws/batch/job` in `ap-northeast-1`, stream prefix `kodefood-gpu`.
11. Create it.

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
