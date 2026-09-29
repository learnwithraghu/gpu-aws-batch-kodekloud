# Video 02 — NVIDIA ECS AMI
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

An AMI is the disk image an EC2 instance boots from. The snapshot, the packages, the agent, the drivers. For GPU work on ECS, AWS publishes ECS-optimized AMIs that already include the ECS agent. The image type ECS_AL2023_NVIDIA adds the NVIDIA kernel drivers and the user-space pieces that agent needs, so a container can be scheduled with a GPU resource. On the create call, that choice is ec2Configuration, image type ECS_AL2023_NVIDIA. It is one field. It is easy to skip in the console. It is painful to debug after you skip it.

A GPU line in the EC2 console only means the hardware is attached to the instance. PyTorch inside the container still asks two questions. Is there a driver on the host, and was a GPU device passed into this container? Boot a plain Amazon Linux AMI on a g4dn and you can spend hours installing drivers, matching kernel modules, and wiring the ECS agent. One wrong package breaks the cluster. The NVIDIA ECS image is the pre-integrated path. You select the image type. You do not become the Linux GPU administrator for a teaching job.

Walk the two boots. Path A is the wrong one for this course. Plain Amazon Linux on a g4dn.xlarge. Billing says the instance has a GPU. The container starts. torch dot cuda dot is_available returns false. The job fails, or worse, it quietly runs the caption on CPU. Path B is the course. The NVIDIA ECS AMI boots. The agent registers the GPU. Batch places a job that asked for one GPU. Inside the container you can see the device slash dev slash nvidia0. CUDA comes back true. BLIP runs on the T4.

Keep the split stack straight. Drivers live on the host, which means the AMI. CUDA libraries and PyTorch live in the image you built, which means the Dockerfile. The container does not replace the AMI. Both layers have to be present, the way a laptop needs both a cable and a live outlet. Lesson one stated that split. This create call is where it becomes a field you can forget.

The job definition still has to ask for one GPU. The scheduler uses that request to pick an instance the agent has marked as GPU-ready. A correct AMI with a job that asks for zero GPUs will not reserve the card. A job that asks for one GPU, placed on a host with no NVIDIA driver, will not see CUDA. Lesson eight can look like a GPU failure when lesson seven stored the wrong image type. When a CUDA check prints false, come back to this field before you rebuild the container.

In this account the Spot environment and the on-demand environment both set that image type. Describe the compute environment and read ec2Configuration before you assume the running host matches the notes. If you ever create the environment because describe came back empty, that image type goes in the same call as the instance type g4dn.xlarge, minimum vCPUs zero, and maximum vCPUs four.

On the screen, two columns. The left column is plain Amazon Linux, and the CUDA check is a red false. The right column is ECS_AL2023_NVIDIA, and the CUDA check is a green true. A small inset shows the job definition asking for GPU equals one, with a line to the sentence the scheduler only places that job on a GPU-ready host.

That host still has to reach ECR, S3, and the model download. Networking is next.
