# Video 02 — NVIDIA ECS AMI
**Type:** Theory
**Runtime target:** ~3 minutes

---

Okay, so what boots underneath the GPU container? An AMI is the disk image an EC2 instance boots from. For GPU work on ECS, AWS publishes ECS-optimized AMIs that already include the ECS agent. The image type ECS_AL2023_NVIDIA adds the NVIDIA drivers the agent needs so a container can be scheduled with a GPU. On the create call that field is ec2Configuration, image type ECS_AL2023_NVIDIA. One field. Easy to skip. Painful after you skip it.

A GPU line in the EC2 console only means the hardware is attached. PyTorch still asks two questions. Is there a driver on the host, and was a GPU passed into this container? Boot plain Amazon Linux on a g4dn and you can spend hours matching drivers and the ECS agent. The NVIDIA ECS image is the integrated path. You select the image type. You do not become the Linux GPU admin for a teaching job.

Path A is wrong for this course. Plain Amazon Linux on a g4dn.xlarge. Billing shows a GPU. The container starts. torch.cuda.is_available returns false. The job fails, or worse, captions on CPU. Path B is the course. The NVIDIA ECS AMI boots. The agent registers the GPU. Batch places a job that asked for one GPU. Inside you see /dev/nvidia0. CUDA is true. BLIP runs on the T4. That is the card KodeFood's photo check needs.

Drivers live on the host, the AMI. CUDA and PyTorch live in the image you built, the Dockerfile. Both must be present. The job definition still asks for one GPU so the scheduler picks a GPU-ready host. A correct AMI with GPU zero will not reserve the card. A GPU one job on a host with no NVIDIA driver will not see CUDA. When a CUDA check prints false, check this field before you rebuild the container.

In this account both Spot and on-demand environments set that image type. Describe and read ec2Configuration. If you create because describe was empty, put that image type in the same call as g4dn.xlarge, min vCPUs zero, max four.

The host still has to reach ECR, S3, and the model download. Networking is next.
