# AWS Batch, one console step at a time

Do these in order. Each folder is one pass in the AWS console. Stay in **Asia Pacific (Tokyo) `ap-northeast-1`**.

This walkthrough creates a new stack named `kodefood-*`. Leave the existing `gpu-teaching-*` resources alone.

| Step | What you create | Done when |
|------|-----------------|-----------|
| [01](01-region-roles-and-network/GUIDE.md) | Nothing. You confirm region, role, and network. | You can name the instance role, VPC, subnet, and security group. |
| [02](02-create-the-compute-environment/GUIDE.md) | CPU compute environment `kodefood-ce` | Status is **VALID** and state is **ENABLED**. |
| [03](03-create-the-job-queue/GUIDE.md) | Job queue `kodefood-queue` | Queue is **VALID** and lists `kodefood-ce`. |
| [04](04-create-the-job-definition/GUIDE.md) | Job definition `kodefood-job` | Revision 1 is **ACTIVE**. |
| [05](05-submit-the-first-job/GUIDE.md) | One job on that queue | Status is **SUCCEEDED** and CloudWatch shows the echo line. |
| [06](06-create-a-gpu-spot-environment/GUIDE.md) | GPU Spot environment `kodefood-gpu-ce-spot` | Status is **VALID**. Minimum vCPUs is **0**. |
| [07](07-create-the-gpu-queue-and-job/GUIDE.md) | Queue `kodefood-gpu-queue` and job `kodefood-gpu-job` | The job definition asks for **1 GPU**. |
| [08](08-submit-the-gpu-job/GUIDE.md) | One GPU smoke job | **SUCCEEDED**, and the log shows a GPU. |
| [09](09-clean-up/GUIDE.md) | Deletes only the `kodefood-*` stack | Queues and compute environments are gone. |

Open [step 01](01-region-roles-and-network/GUIDE.md).
