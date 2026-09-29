# Video 09 — Demo: Batch environment setup
**Type:** Demo
**Runtime target:** ~3 minutes

---

Okay, so let's walk describe before create on a real terminal. You have an image in ECR and photos in S3. Batch still will not start a GPU until three things exist. A compute environment, the pool. A job queue, where you send work. A job definition, the template: image, memory, one GPU, and which role can touch S3.

This clip is setup, not the job. Look before you create. A second compute environment with a different name is a second pool you pay for when jobs land on it.

I am in the terminal. Region ap-northeast-1. I source the env file so the account, image URI, and job role are in the shell.

First, the Spot compute environment gpu-teaching-gpu-smoke-ce-spot. I run describe-compute-environments. I want status VALID. Instance type g4dn.xlarge. Min vCPUs zero. Max four, one machine. If INVALID, I read statusReason before I create anything else.

If describe is empty, I create once. Same limits, Spot, course subnet and security group. The field to notice is image type ECS_AL2023_NVIDIA. That AMI has the NVIDIA drivers. Plain Amazon Linux on a g4dn can look like a GPU machine and still leave CUDA invisible. After create I describe again and wait for VALID. That can take a minute or two.

Next, the queue gpu-teaching-gpu-smoke-queue-spot. I want ENABLED and VALID, with compute environment order pointing at the Spot environment. Jobs on this queue stay on that pool. They do not hop to on-demand because Spot is quiet. If the queue is missing, I create it only after the environment is VALID, and bind it in the same command.

Last, job definition gpu-teaching-caption-job. I describe active definitions and look at the highest revision. Image should be the ECR URI we pushed. Memory twelve thousand two hundred eighty-eight mebibytes. One GPU and four vCPUs. Job role ARN filled in. Logs use awslogs to /aws/batch/job. If there is no active revision, or image, memory, GPU, role, or logs are wrong, I register once. Register always makes a new revision. When we submit we pass the name and let Batch pick the highest active revision. We do not pin revision one or two.

Before I stop: environment VALID, queue enabled and bound, job definition active with one GPU, right memory, and a job role. Lesson eight is the submit. Overrides choose the vendor folder. This template chooses the machine.
