# Video 01 — Managed compute environments
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

The image is in ECR and the photos are in S3. Neither of those starts a GPU. A compute environment is the pool of machines your jobs are allowed to use. In a managed compute environment, AWS Batch creates, connects, and scales the EC2 instances for you, through ECS. You supply the constraints. Instance types. Minimum and maximum vCPUs. Spot or on demand. A subnet, a security group, and an AMI type. Batch turns queue depth into desired capacity. You do not SSH in to install a driver for an ordinary job. You pick the AMI type that already has what ECS needs, and you submit containers.

Someone still has to launch machines, join them to a cluster, and scale them down when the queue is empty. A managed environment moves that someone from your on-call notes to the Batch control plane. It is the same reason a team uses a node group instead of hand-provisioning a VM for every cron job. The object you keep is one API resource. The instances come and go behind it.

The environment this course actually uses is named gpu-teaching-gpu-smoke-ce-spot. It is managed, and it is enabled. The purchase type is Spot, with the allocation strategy SPOT_CAPACITY_OPTIMIZED. Minimum vCPUs is zero, so an idle class costs no GPU hours. Maximum vCPUs is four. The only instance type is g4dn.xlarge, one NVIDIA T4 and four vCPUs, so that maximum is one machine, not a classroom full of them. The image type on the compute resources is ECS_AL2023_NVIDIA, which is the next clip. The instance profile is ecsInstanceRole. That profile lets the host pull from ECR and write logs. It does not get S3.

When a job sits on the queue, Batch raises desired vCPUs toward four, which brings up one instance. When the queue empties, desired falls back toward zero. You do not name this environment on the submit call. You name a queue, and the queue is bound to the environment. The Spot queue is gpu-teaching-gpu-smoke-queue-spot. There is a second environment for on demand, gpu-teaching-gpu-smoke-ce-on-demand, same instance type, same vCPU limits, purchase type EC2 instead of Spot. Jobs do not hop from one to the other because one of them is quiet.

An unmanaged compute environment is the other shape, and this course does not use it. Unmanaged means you already run the ECS cluster, and Batch only places work onto it. Managed is the teaching default. One object, one mental model, Batch owns the cluster lifecycle.

Do not create a second pool to practice the console. Each compute environment has its own maximum vCPU budget, and each one can scale when jobs arrive. A duplicate name is a second bill. Lesson seven describes the smoke environment that already exists, and creates it only when describe says the name is missing.

On the screen, a graph of queue depth runs along the top. Under it, EC2 bars appear when the depth is above zero, and they disappear when the depth returns to zero. The caption is simple. Managed means AWS scales ECS and EC2 for this environment.

The AMI on those instances is what makes the GPU visible to CUDA. That choice is next.
