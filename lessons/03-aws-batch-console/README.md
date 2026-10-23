# Section 003 — AWS Batch console demos

Three console-only demos for **Section 003: AWS Batch: Scaling GPU Workloads**.  
No demo transcripts — these runbooks are the steps.

Region: **Asia Pacific (Tokyo) `ap-northeast-1`**.

Videos: [`transcript/003-aws-batch-scaling-gpu-workloads/`](../../transcript/003-aws-batch-scaling-gpu-workloads/).  
Live inventory: [`docs/aws-batch-setup.md`](../../docs/aws-batch-setup.md).

## Demo map

| CSV # | Title | Runbook |
|-------|--------|---------|
| 004 | [Demo] Create the Batch control plane | [004-create-the-batch-control-plane.md](004-create-the-batch-control-plane.md) |
| 006 | [Demo] Job definition and dummy job | [006-job-definition-and-dummy-job.md](006-job-definition-and-dummy-job.md) |
| 015 | [Demo] Run a GPU job on Spot | [015-run-a-gpu-job-on-spot.md](015-run-a-gpu-job-on-spot.md) |

## Hybrid resources

| Prefix | Demos | Rule |
|--------|-------|------|
| `kk-batch-demo-*` | 004, 006 | Create and delete in console |
| `gpu-teaching-*` | 015 | **Reuse only** — do not recreate live smoke/caption resources |

### Demo stack (004 / 006)

| Object | Name |
|--------|------|
| Launch template | `kk-batch-demo-lt` |
| Compute environment | `kk-batch-demo-ce-cpu` |
| Job queue | `kk-batch-demo-queue-cpu` |
| Job definition | `kk-batch-demo-job` |

### Live GPU stack (015)

| Object | Name |
|--------|------|
| GPU Spot CE | `gpu-teaching-gpu-smoke-ce-spot` |
| GPU Spot queue | `gpu-teaching-gpu-smoke-queue-spot` |
| GPU smoke job def | `gpu-teaching-gpu-smoke-job` |
| On-demand fallback queue | `gpu-teaching-gpu-smoke-queue-on-demand` |

## Prerequisites (once)

1. Console region **Tokyo (`ap-northeast-1`)**.
2. Instance profile **`ecsInstanceRole`** with `AmazonEC2ContainerServiceforEC2Role`.
3. Batch service-linked role `AWSServiceRoleForBatch` (created on first CE if missing).
4. Network: VPC `vpc-3f0b1a58`, subnet `subnet-b560b3fd`, SG `sg-bd00e4f5`.
5. CloudWatch log group `/aws/batch/job`.

## Cost

- Minimum vCPUs **0** on every CE.
- Prefer Spot for GPU. On-demand G/VT quota on this teaching account is often **0**.

## Cleanup (`kk-batch-demo-*` only)

1. Confirm no demo jobs are `RUNNING`.
2. Disable → delete queue `kk-batch-demo-queue-cpu`.
3. Disable → delete CE `kk-batch-demo-ce-cpu`.
4. Deregister job definition `kk-batch-demo-job`.
5. Delete launch template `kk-batch-demo-lt`.

Do **not** delete live `gpu-teaching-*` resources.
