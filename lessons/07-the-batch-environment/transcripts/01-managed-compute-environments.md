# Video 01 — Managed compute environments
**Type:** Theory
**Runtime target:** ~3 minutes

---

Hello. The image is in ECR and the photos are in S3. Neither starts a GPU. A compute environment is the pool of machines your jobs may use. In a managed one, Batch creates and scales EC2 through ECS. You set instance types, min and max vCPUs, Spot or on demand, a subnet, a security group, and an AMI type. Batch turns queue depth into desired capacity. You do not SSH in to install a driver. You pick the AMI type that already has what ECS needs, and you submit containers.

The environment this course uses is gpu-teaching-gpu-smoke-ce-spot. It is managed and enabled. Purchase type is Spot with SPOT_CAPACITY_OPTIMIZED. Minimum vCPUs is zero, so idle time costs no GPU hours. Maximum vCPUs is four. The only instance type is g4dn.xlarge, one T4 and four vCPUs, so that maximum is one machine. The image type is ECS_AL2023_NVIDIA. The instance profile is ecsInstanceRole. That profile pulls from ECR and writes logs. It does not get S3.

When a KodeFood vendor folder sits on the queue, Batch raises desired vCPUs toward four and brings up one instance. When the queue empties, desired falls toward zero. You do not name this environment on submit. You name a queue bound to it. The Spot queue is gpu-teaching-gpu-smoke-queue-spot. There is an on-demand twin, gpu-teaching-gpu-smoke-ce-on-demand, same instance type and vCPU limits, purchase type EC2. Jobs do not hop lanes because one pool is quiet.

Unmanaged means you already run the ECS cluster and Batch only places work. This course uses managed. Do not create a second pool to practice. Each environment has its own max vCPU budget. A duplicate name is a second bill. Create only when describe says the name is missing.

The AMI is what makes CUDA visible. That choice is next.
