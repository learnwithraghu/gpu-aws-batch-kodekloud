# Lesson 07 — Theory

This lesson turns ECR + S3 into a schedulable GPU pool. Describe before you create.

## Managed compute environments

A **managed** compute environment lets Batch create and scale ECS capacity for you. You choose instance types, purchase option, VPC networking, and limits (`minvCpus`, `maxvCpus`). Batch owns the ECS cluster lifecycle behind the scenes.

You do not SSH in to install the NVIDIA driver for everyday jobs. You pick an AMI type that already includes what ECS needs for GPUs, then submit containers.

## NVIDIA ECS AMI

`ECS_AL2023_NVIDIA` (via `ec2Configuration.imageType`) gives the ECS agent plus NVIDIA drivers on the host.

A plain Amazon Linux AMI on a `g4dn` can look “GPU shaped” in EC2 and still leave `torch.cuda.is_available()` false inside the container. Drivers live on the host; CUDA libraries live in the image; both must be present. Lesson 01 stated this; the create call here is where it becomes real.

## Networking for GPU jobs

The instance needs a path to:

- **ECR** — pull `gpu-teaching:latest`
- **S3** — list/get photos, put the CSV
- **Hugging Face (or similar)** — first-time model weight download inside the container

This course uses a public subnet with a public IP so those endpoints are reachable without private VPC endpoints. Security groups must allow the egress the job needs. Wrong subnet or locked-down egress shows up as pull timeouts or model download failures, not as a Python syntax error.

## Service-linked role vs instance profile vs job role

Three IAM actors:

| Actor | Who | Job |
|-------|-----|-----|
| `AWSServiceRoleForBatch` | Batch service | Create/scale ECS capacity |
| Instance profile (`ecsInstanceRole`) | EC2 host | ECR pull, CloudWatch logs |
| Job role (`gpu-teaching-batch-job-role`) | Container task | S3 read/write for the catalog |

Confusing them causes sharp failures: CE `INVALID`, image pull denied, or `AccessDenied` on S3 after the GPU already started.

## Job definition as a contract

The job definition is the template Batch places:

- Image URI (ECR)
- vCPU, memory, GPU counts
- `jobRoleArn`
- Default command (here a small CUDA check)
- Optional default environment

Lesson 08 overrides the command to `python /app/describe_items.py` and sets `IMAGE_PREFIX`. The definition still must request **1 GPU** and **12288** MiB so placement succeeds.

## Revisions

Every `register-job-definition` call creates a new **revision**, even if nothing changed. Submit by name uses the highest active revision unless you pin one.

In this course:

- `:1` — 16384 MiB → never places
- `:2` — no job role → S3 fails
- `:3`+ — usable pattern (memory + role)

Do not “fix” a bad revision by re-registering blindly without checking; you can leave students on a broken latest if you are careless. Describe first.

## Queue ↔ CE binding

A job queue points at one or more compute environments. Jobs on that queue only run on those environments.

Spot queue → Spot CE. On-demand queue → on-demand CE. Submitting to the Spot queue never magically uses on-demand capacity. When Spot is dry, change the queue (or bind a second CE), do not only stare at the job definition.

## Describe-before-create

`describe-*` returning a healthy resource means skip create. A second CE with a new name is a second pool: another max vCPU budget and another billable path.

Course hygiene: reuse `gpu-teaching-gpu-smoke-*` names that already exist. Create only when describe says the name is missing. Duplicate “learning” environments are how idle GPU capacity surprises you on the invoice.
