# Video 02 — NVIDIA ECS AMI
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What it is.** An **AMI** (Amazon Machine Image) is the **disk snapshot and configuration** an EC2 instance boots from. For GPU workloads on ECS, AWS publishes **ECS-optimized AMIs** that already include the ECS agent. The **`ECS_AL2023_NVIDIA`** image type adds **NVIDIA kernel drivers and the user-space pieces the agent needs** so containers can be scheduled with GPU resources.

**Why it exists.** A GPU in the EC2 console is only **hardware attached to the instance**. PyTorch inside Docker still asks: “Is there a driver on the host, and is a GPU device passed into my container?” If you boot a generic Linux AMI on a `g4dn`, you might spend hours installing drivers, matching kernel modules, and configuring the ECS agent — and one wrong package breaks the cluster. AWS sells a **pre-integrated path** so Batch users pick **`imageType: ECS_AL2023_NVIDIA`** in **`ec2Configuration`** instead of becoming Linux GPU sysadmins.

**Example — two boot sequences on screen.** **Path A (wrong for us):** plain Amazon Linux on `g4dn` → instance “has GPU” in billing → container starts → `torch.cuda.is_available()` returns **False** → job fails or runs on CPU by mistake. **Path B (course):** NVIDIA ECS AMI → agent registers GPU → Batch places `GPU=1` job → container sees **`/dev/nvidia0`** → CUDA true → BLIP runs on the T4.

Remember the **split stack**: **drivers on the host** (AMI), **CUDA libraries and PyTorch in the image** (your Dockerfile). The container does not replace the AMI; both layers must agree, like needing both a charging cable and a wall outlet.

**In this course.** The create-compute-environment call sets **`ec2Configuration`** with **`ECS_AL2023_NVIDIA`**. That single field is easy to skip in the console and painful to debug if omitted — lesson eight “GPU job failed” might be lesson seven “wrong AMI type.”

**Visual:** Two-column boot diagram; green check only on NVIDIA ECS path. Small inset of job definition **`GPU=1`** connecting to “scheduler only picks GPU-ready instances.”

Networking must let that instance pull images and model weights — next.
