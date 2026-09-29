# Video 01 — Managed compute environments
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What it is.** A **compute environment** in AWS Batch is the **pool of machines** your jobs are allowed to use. In a **managed** compute environment, AWS Batch (through ECS) **creates, connects, and scales** EC2 instances for you. You supply constraints — instance types, minimum and maximum vCPUs, Spot or on-demand, subnets, security groups, AMI type — and Batch turns queue depth into **desired capacity**.

**Why it exists.** Batch jobs need real hardware. Someone has to launch EC2, join an ECS cluster, install or select the right AMI, and scale down when work finishes. Managed CEs move that “someone” from your on-call engineer to the Batch control plane — the same reason companies use Kubernetes node groups instead of hand-provisioning VMs per cron job.

**Example.** Imagine a compute environment named **`gpu-teaching-gpu-smoke-ce-spot`**. You configure: **`minvCpus=0`** so idle cost goes to zero; **`maxvCpus`** capped so a classroom cannot accidentally request fifty GPUs; **`instanceTypes=[g4dn.xlarge]`** so only T4-sized boxes appear; **`allocationStrategy`** appropriate for Spot; **`ec2Configuration`** with **`ECS_AL2023_NVIDIA`** so drivers exist on the host. When a job sits in the queue, Batch raises **desired vCPUs** toward four (one instance). When the queue empties, desired returns toward zero.

**Unmanaged** compute environments (not used here) mean **you** already run an ECS cluster and Batch only places work onto it. Managed is the teaching default: one API object, one mental model.

**In this course.** Lesson seven either **describes** an existing smoke CE or **creates** it once. Jobs never reference the CE by name at submit time — they go through a **queue** bound to that CE. Students should not create duplicate CEs “for practice”; each CE is a billing and capacity path.

**Visual:** Batch queue depth graph on top; below, EC2 instances appearing as bars when depth > 0, disappearing at zero. Label “managed = AWS scales ECS/EC2 for this CE.”

The NVIDIA AMI choice is what makes those instances actually usable for CUDA — next.
