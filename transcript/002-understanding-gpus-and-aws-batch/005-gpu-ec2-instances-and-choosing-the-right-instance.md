# Video 005 — GPU EC2 Instances and Choosing the Right Instance
**Section:** 002 — Understanding GPUs and AWS Batch
**Lecture#:** 005
**Sheet title:** GPU EC2 Instances and Choosing the Right Instance
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 002-005-gpu-ec2-instances-and-choosing

---

A compute environment can only place our job if the instance family, the host AMI, and the job’s resource request all agree. Let’s look at how we choose the right GPU instance for KodeFood.

AWS offers several GPU instance families. `g4dn` instances pair NVIDIA T4 GPUs with balanced CPU and host memory, making them a cost-effective workhorse for image inference. `g5` instances step up to NVIDIA A10G GPUs for heavier models at a higher hourly price, while `p`-series families target large-scale training and multi-GPU clusters—far more hardware than thirty menu photos need.

For this course, we use `g4dn.xlarge`: one NVIDIA T4 GPU with 16 GiB of VRAM, 4 vCPUs, and 16 GiB of host system memory. One catalog job claims that entire instance—4 vCPUs and 1 GPU—so we never pack competing GPU jobs onto the same machine.

Three placement details must line up on that `g4dn.xlarge`. First, the compute environment uses the `ECS_AL2023_NVIDIA` AMI so the host boots with NVIDIA drivers and the ECS container agent ready. Second, the job definition requests `GPU=1`. Third, the job definition requests `12288` MiB of memory—not the full `16384` MiB on the datasheet. The operating system and ECS agent reserve a slice of host RAM. If a job definition asks for all 16384 MiB, no `g4dn.xlarge` can satisfy it, and the job sits in `RUNNABLE` forever with a resource misconfiguration reason.

The rule of thumb in production is simple: pick the smallest GPU instance that fits your model and latency target, and size container memory below the host’s usable ceiling.

Next, we’ll look at how we pay for that `g4dn.xlarge`—Spot versus on-demand—and how AWS GPU quotas affect both.

---

## Further reading (not spoken)

- https://aws.amazon.com/ec2/instance-types/g4/ — Amazon EC2 G4 instance family (`g4dn`) specs
- https://aws.amazon.com/ec2/instance-types/g5/ — Amazon EC2 G5 instance family for comparison
- https://docs.aws.amazon.com/batch/latest/userguide/gpu-jobs.html — GPU scheduling and AMI requirements in AWS Batch
