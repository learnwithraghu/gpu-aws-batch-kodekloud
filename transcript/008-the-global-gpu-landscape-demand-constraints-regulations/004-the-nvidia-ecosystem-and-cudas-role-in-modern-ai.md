# Video 004 — The NVIDIA Ecosystem and CUDA's Role in Modern AI

**Section:** 008 — The Global GPU Landscape: Demand, Constraints & Regulations
**Lecture#:** 004
**Sheet title:** The NVIDIA Ecosystem and CUDA's Role in Modern AI
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 008-004-the-nvidia-ecosystem-and-cu

---

The KodeFood stack uses a PyTorch CUDA base image, BLIP through Transformers, and drivers from the ECS GPU-optimized AMI. This is not a generic accelerator stack. It belongs to the NVIDIA ecosystem, with CUDA at its center.

CUDA provides compilers, libraries, and a programming model for NVIDIA GPUs. cuDNN accelerates deep-learning operations. NCCL supports communication in multi-GPU training. TensorRT optimizes inference graphs. PyTorch and TensorFlow use these paths on NVIDIA hardware. In this stack, “run on GPU” usually means scheduling kernels through CUDA.

This creates ecosystem gravity. Engineers learn CUDA tools, software vendors certify against NVIDIA, and cloud providers stock NVIDIA instances. Alternatives such as ROCm, oneAPI, and AWS Neuron exist, but moving requires porting and validation. CUDA remains the shortest path for many Hugging Face applications.

NVIDIA reinforces the ecosystem with DGX systems, NGC containers, and AI Enterprise software. Competitors and regulators pay attention because the hardware and software advantages strengthen each other.

KodeFood uses CUDA because BLIP, PyTorch, and the AWS GPU AMI already agree on that interface. That compatibility is infrastructure. It also means shortages or export controls affecting NVIDIA-class accelerators can affect the application even when the hardware is rented through AWS.

The software path narrows the hardware choices. Next we look at how those choices vary across Regions and cloud providers.

---

## Further reading (not spoken)

- [NVIDIA CUDA](https://www.nvidia.com/en-us/data-center/cuda/) — platform overview
- [NVIDIA cuDNN](https://developer.nvidia.com/cudnn) — deep learning primitives library
- [PyTorch CUDA semantics](https://pytorch.org/docs/stable/notes/cuda.html) — how PyTorch binds to CUDA devices
- [AWS Deep Learning AMIs](https://docs.aws.amazon.com/dlami/latest/devguide/what-is-dlami.html) — prebuilt CUDA/driver stacks on EC2
