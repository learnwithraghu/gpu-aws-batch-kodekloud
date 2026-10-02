# Video 002 — NVIDIA ECS-Optimized AMIs and GPU Drivers

**Section:** 005 — Building the AWS Batch GPU Infrastructure
**Lecture#:** 002
**Sheet title:** NVIDIA ECS-Optimized AMIs and GPU Drivers
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 005-002-nvidia-ecs-optimized-amis-and-

---

Suppose Batch launches a `g4dn.xlarge`, but `torch.cuda.is_available()` is false. The instance type is correct, so the next check is the AMI: the machine image that boots before the container exists.

GPU containers do not supply the host driver. PyTorch and CUDA inside the image talk through the container runtime to the NVIDIA driver on the host. If that driver is missing, or the stack is incompatible, CUDA detection fails even though the machine has a T4.

That is why our compute environments use an NVIDIA ECS-optimized AMI. In the live setup, this is the Amazon Linux 2023 NVIDIA ECS variant, `ECS_AL2023_NVIDIA`. It includes the ECS agent and NVIDIA driver, and exposes the GPU to containers that request it. We are not installing drivers by hand on every cold start.

Keep the responsibility split clear. The AMI owns the host driver and ECS agent. The ECR image owns the application, PyTorch, and the matching CUDA user-space libraries. If either side is wrong, the caption job can fail before BLIP loads a photo.

This is the standard GPU-container contract: driver on the host, user-space libraries in the image. The managed Batch environment gives us an AMI that already supports that contract.

In the lab, use two checks. A successful `nvidia-smi` smoke job proves the host side. When `describe_items.py` sees CUDA, it also proves the image side.

With the GPU path established, we can separate the three IAM roles. Each role has a different responsibility and a different failure symptom.

---

## Further reading (not spoken)

- [Amazon ECS-optimized Linux AMIs](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html) — including NVIDIA GPU variants
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/index.html) — how containers access the host GPU
- [AWS Batch: GPU jobs](https://docs.aws.amazon.com/batch/latest/userguide/gpu-jobs.html) — requiring GPUs on Batch jobs
