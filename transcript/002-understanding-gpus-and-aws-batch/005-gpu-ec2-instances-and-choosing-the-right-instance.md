# Video 005 — GPU EC2 Instances and Choosing the Right Instance
**Section:** 002 — Understanding GPUs and AWS Batch
**Lecture#:** 005
**Sheet title:** GPU EC2 Instances and Choosing the Right Instance
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 002-005-gpu-ec2-instances-and-choosing

---

The compute environment can only place our job if we choose an instance shape that matches it. Let’s make that choice deliberately.

AWS has several GPU families. `g4dn` instances pair NVIDIA T4 GPUs with useful amounts of host memory and suit inference and graphics workloads. `g5` instances use NVIDIA A10G GPUs for more performance, usually at higher cost. Training-oriented families also exist, but they are more capacity than we need for thirty menu photos.

KodeFood uses `g4dn.xlarge`: four vCPUs, sixteen GiB of host memory, and one T4 GPU. That is enough for BLIP with micro-batches of eight. The job definition requests one GPU and twelve thousand two hundred eighty-eight MiB of container memory. We do not request sixteen thousand three hundred eighty-four MiB, because the host must reserve memory for the operating system and ECS agent.

The selection rule is straightforward. Match the GPU to the model and latency target. Leave enough host memory for both the container and operating system. Then choose the smallest instance that finishes the folder comfortably. Moving to `g5` without measurements adds cost before it solves a demonstrated problem.

In this course, one catalog job owns the whole `g4dn.xlarge`. We do not pack several GPU jobs onto one instance. That keeps placement behavior easier to reason about.

The instance shape is set. Next, we’ll decide whether to obtain that `g4dn` capacity through Spot or on-demand.

---

## Further reading (not spoken)

- https://aws.amazon.com/ec2/instance-types/g4/ — G4 instance family and T4 positioning
- https://aws.amazon.com/ec2/instance-types/g5/ — G5 family for contrast
- https://www.nvidia.com/en-us/data-center/tesla-t4/ — T4 as an inference-oriented GPU
