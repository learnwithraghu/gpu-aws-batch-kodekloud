# Video 002 — NVIDIA ECS-Optimized AMIs and GPU Drivers

**Section:** 005 — Building the AWS Batch GPU Infrastructure
**Lecture#:** 002
**Sheet title:** NVIDIA ECS-Optimized AMIs and GPU Drivers
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 005-002-nvidia-ecs-optimized-amis-and-

---

Batch can launch an instance and still give you a useless GPU box. The difference is the AMI — the machine image that boots before your container exists.

GPU containers do not ship the host driver. PyTorch and CUDA inside the image talk to the NVIDIA driver on the host through the container runtime. If the host has no driver, or an incompatible stack, `torch.cuda.is_available()` fails even though you paid for a T4.

That is why our compute environments use an NVIDIA ECS-optimized AMI — in the live setup, the Amazon Linux 2023 NVIDIA ECS variant. It is built for ECS and Batch: the ECS agent is there, the NVIDIA driver is there, and the GPU is visible to containers that request it. You are not installing drivers by hand on every cold start.

Notice the split of responsibility. The AMI owns host drivers and the agent. Your ECR image owns the application, PyTorch, and the CUDA user-space libraries that match that stack. Get either side wrong and the caption job dies before BLIP loads a single photo.

This pattern shows up anywhere teams run GPU containers on EC2 or ECS. NVIDIA’s own container guidance assumes a driver on the host and libraries in the image. AWS Batch managed environments simply pick an AMI that already follows that contract so you can focus on the job definition.

For KodeFood, treat the AMI as part of the infrastructure contract, not as an afterthought. When a smoke job runs `nvidia-smi` successfully, you have proven the host side. When `describe_items.py` sees CUDA, you have proven the image side as well.

That’s it here for the AMI and drivers. Next we separate three IAM roles — service, instance, and job — because each one fails differently when it is missing.

---

## Further reading (not spoken)

- [Amazon ECS-optimized Linux AMIs](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html) — including NVIDIA GPU variants
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/index.html) — how containers access the host GPU
- [AWS Batch: GPU jobs](https://docs.aws.amazon.com/batch/latest/userguide/gpu-jobs.html) — requiring GPUs on Batch jobs
