# Project instructions

These instructions apply in any agent. Do not keep a second copy in an editor-specific folder.

## AWS Batch setup (do not re-discover)

Full inventory: [`docs/aws-batch-setup.md`](docs/aws-batch-setup.md).
Read that file instead of querying AWS unless the user says infra changed.
Account ID, bucket suffixes, and ECR registry come from local `.env` — never
commit them.

### Defaults (region `ap-northeast-1`)

- Queue: `gpu-teaching-gpu-smoke-queue-spot` (fallback: `gpu-teaching-gpu-smoke-queue-on-demand`)
- Job definition: `gpu-teaching-caption-job` — use revision **4+** (12288 MiB, job role, explicit `awslogs` → `/aws/batch/job`). Revision **1 is broken** (16384 MiB never places). Revision **2** has no `jobRoleArn`. Revision **3** has the job role but no explicit `logConfiguration`.
- Image: `<account-id>.dkr.ecr.ap-northeast-1.amazonaws.com/gpu-teaching:latest` (from `ECR_IMAGE_URI`)
- Images: `s3://gpu-teaching-images-<account-id>/images/<stem>/` (vendor food photos, ~25–30 per folder)
- Catalog CSV: `s3://gpu-teaching-captions-csv-<account-id>/descriptions/<stem>/descriptions.csv` (`image_s3_uri`, `item_description`)
- Logs: `/aws/batch/job`
- Network (already wired into the compute environments): VPC `vpc-3f0b1a58`, subnet `subnet-b560b3fd` (`ap-northeast-1a`), SG `sg-bd00e4f5`
- Instance profile: `ecsInstanceRole` (ECR pull and logs only). Container S3 uses `gpu-teaching-batch-job-role` via `jobRoleArn` (`BATCH_JOB_ROLE_ARN` in `.env`). The name `BatchJobRole` is not live.

### Do not

- Recreate `gpu-teaching-ce` / `gpu-teaching-queue` / `gpu-teaching-job-def` (those names are not the live resources).
- Register a job definition with 16384 MiB memory on `g4dn.xlarge`.
- Put AWS keys or account IDs in the repo. CLI credentials stay in `~/.aws/` via `aws configure`.
- Recreate or delete the live `gpu-teaching-*` stack while following `02-aws-batch/`. That walkthrough uses a separate `kodefood-*` stack.
- Assume a container program still lives in this repo. The course revision is the restaurant portal plus console guides. Batch still runs whatever image was last pushed to ECR.

### Stuck jobs

- `RUNNABLE` forever → Spot capacity, or on-demand G/VT quota is 0 (`L-DB2E81BA`); stay on Spot until that quota is ≥ 4.
- `MISCONFIGURATION:JOB_RESOURCE_REQUIREMENT` → wrong memory; keep GPU jobs at 12288 MiB or below on `g4dn.xlarge`. The 16384 MiB revision never places.
- Container exit 1 → CloudWatch `/aws/batch/job` first.

## Skills

Lecture transcripts, video scripts, demo scripts, and lab runbooks follow [`.agents/skills/tone/SKILL.md`](.agents/skills/tone/SKILL.md).
