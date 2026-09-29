# Lesson 07 — Create the Batch environment

You already have an image in ECR and two buckets. This lesson attaches a GPU machine pool, a queue, and a job definition. Create a piece only when the describe command says it is missing. This account already has these names. A second copy with a different name is a different pool you will pay for.

Theory reading: [`theory.md`](theory.md).

```bash
set -a && source .env && set +a
export AWS_DEFAULT_REGION=ap-northeast-1
export ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
```

Network already used by the live environments: subnet `subnet-b560b3fd` (`ap-northeast-1a`), security group `sg-bd00e4f5`.

## 1. Instance role

The EC2 instance pulls the image and writes logs. It does not get S3 access.

```bash
aws iam get-instance-profile --instance-profile-name ecsInstanceRole
```

If that profile is missing, create it once:

```bash
aws iam create-role --role-name ecsInstanceRole \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "ec2.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

aws iam attach-role-policy --role-name ecsInstanceRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role

aws iam create-instance-profile --instance-profile-name ecsInstanceRole
aws iam add-role-to-instance-profile \
  --instance-profile-name ecsInstanceRole \
  --role-name ecsInstanceRole
```

Batch’s own service-linked role is created the first time you make a compute environment. If creation complains that it is missing:

```bash
aws iam create-service-linked-role --aws-service-name batch.amazonaws.com
```

## 2. Job role

The container assumes this role to read photos and write the CSV.

```bash
aws iam get-role --role-name gpu-teaching-batch-job-role
```

If the role is missing:

```bash
aws iam create-role --role-name gpu-teaching-batch-job-role \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "ecs-tasks.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

aws iam put-role-policy --role-name gpu-teaching-batch-job-role \
  --policy-name gpu-teaching-batch-job-s3 \
  --policy-document "{
    \"Version\": \"2012-10-17\",
    \"Statement\": [
      {
        \"Effect\": \"Allow\",
        \"Action\": [\"s3:ListBucket\"],
        \"Resource\": [
          \"arn:aws:s3:::${S3_IMAGES_BUCKET}\",
          \"arn:aws:s3:::${S3_CSV_BUCKET}\"
        ]
      },
      {
        \"Effect\": \"Allow\",
        \"Action\": [\"s3:GetObject\"],
        \"Resource\": \"arn:aws:s3:::${S3_IMAGES_BUCKET}/*\"
      },
      {
        \"Effect\": \"Allow\",
        \"Action\": [\"s3:GetObject\", \"s3:PutObject\"],
        \"Resource\": \"arn:aws:s3:::${S3_CSV_BUCKET}/*\"
      }
    ]
  }"
```

Write the ARN into `.env`:

```bash
BATCH_JOB_ROLE_ARN=arn:aws:iam::${ACCOUNT_ID}:role/gpu-teaching-batch-job-role
```

## 3. GPU Spot compute environment

```bash
aws batch describe-compute-environments \
  --compute-environments gpu-teaching-gpu-smoke-ce-spot \
  --query 'computeEnvironments[0].{status:status,type:computeResources.type,instances:computeResources.instanceTypes}'
```

An empty result means it does not exist yet. Create it with the NVIDIA AMI, Spot, and a cap of 4 vCPU (one `g4dn.xlarge`):

```bash
aws batch create-compute-environment \
  --compute-environment-name gpu-teaching-gpu-smoke-ce-spot \
  --type MANAGED \
  --state ENABLED \
  --compute-resources "{
    \"type\": \"SPOT\",
    \"allocationStrategy\": \"SPOT_CAPACITY_OPTIMIZED\",
    \"minvCpus\": 0,
    \"maxvCpus\": 4,
    \"instanceTypes\": [\"g4dn.xlarge\"],
    \"subnets\": [\"subnet-b560b3fd\"],
    \"securityGroupIds\": [\"sg-bd00e4f5\"],
    \"instanceRole\": \"arn:aws:iam::${ACCOUNT_ID}:instance-profile/ecsInstanceRole\",
    \"ec2Configuration\": [{\"imageType\": \"ECS_AL2023_NVIDIA\"}]
  }"
```

Wait until `status` is `VALID` (a minute or two):

```bash
aws batch describe-compute-environments \
  --compute-environments gpu-teaching-gpu-smoke-ce-spot \
  --query 'computeEnvironments[0].status' --output text
```

`INVALID` means the subnet, security group, instance profile, or service role is wrong. Read `statusReason` on the same describe call before you create anything else.

On-demand fallback, same shape, different purchasing option. Create it only if describe says it is missing:

```bash
aws batch create-compute-environment \
  --compute-environment-name gpu-teaching-gpu-smoke-ce-on-demand \
  --type MANAGED \
  --state ENABLED \
  --compute-resources "{
    \"type\": \"EC2\",
    \"minvCpus\": 0,
    \"maxvCpus\": 4,
    \"instanceTypes\": [\"g4dn.xlarge\"],
    \"subnets\": [\"subnet-b560b3fd\"],
    \"securityGroupIds\": [\"sg-bd00e4f5\"],
    \"instanceRole\": \"arn:aws:iam::${ACCOUNT_ID}:instance-profile/ecsInstanceRole\",
    \"ec2Configuration\": [{\"imageType\": \"ECS_AL2023_NVIDIA\"}]
  }"
```

## 4. Job queues

```bash
aws batch describe-job-queues \
  --job-queues gpu-teaching-gpu-smoke-queue-spot \
  --query 'jobQueues[0].status' --output text
```

If it is missing, wait until the compute environment is `VALID`, then:

```bash
aws batch create-job-queue \
  --job-queue-name gpu-teaching-gpu-smoke-queue-spot \
  --state ENABLED \
  --priority 1 \
  --compute-environment-order order=1,computeEnvironment=gpu-teaching-gpu-smoke-ce-spot
```

Same for the fallback queue, after its compute environment is `VALID`:

```bash
aws batch create-job-queue \
  --job-queue-name gpu-teaching-gpu-smoke-queue-on-demand \
  --state ENABLED \
  --priority 1 \
  --compute-environment-order order=1,computeEnvironment=gpu-teaching-gpu-smoke-ce-on-demand
```

Wait until the queue status is `VALID`.

```bash
BATCH_JOB_QUEUE=gpu-teaching-gpu-smoke-queue-spot
```

## 5. Job definition

The definition is the template lesson 08 submits. Memory stays at **12288**. GPU is **1**. The image is the URI you pushed in lesson 04. The job role is the role from step 2.

Stdout and stderr go to CloudWatch via the `awslogs` driver. Create the log group once (safe to re-run):

```bash
aws logs create-log-group --log-group-name /aws/batch/job --region "$AWS_DEFAULT_REGION" 2>/dev/null || true
```

Look at the highest active revision first:

```bash
aws batch describe-job-definitions \
  --job-definition-name gpu-teaching-caption-job \
  --status ACTIVE \
  --query 'sort_by(jobDefinitions, &revision)[-1].{revision:revision,image:containerProperties.image,req:containerProperties.resourceRequirements,role:containerProperties.jobRoleArn,logs:containerProperties.logConfiguration}'
```

Register a new revision only when there is no active revision, or the image, memory, GPU, role, or logging config is wrong. Every register call creates another revision even when nothing changed.

```bash
aws batch register-job-definition \
  --job-definition-name gpu-teaching-caption-job \
  --type container \
  --container-properties "{
    \"image\": \"${ECR_IMAGE_URI}\",
    \"jobRoleArn\": \"${BATCH_JOB_ROLE_ARN}\",
    \"resourceRequirements\": [
      {\"type\": \"VCPU\", \"value\": \"4\"},
      {\"type\": \"MEMORY\", \"value\": \"12288\"},
      {\"type\": \"GPU\", \"value\": \"1\"}
    ],
    \"environment\": [
      {\"name\": \"S3_BUCKET\", \"value\": \"${S3_BUCKET}\"},
      {\"name\": \"S3_CSV_BUCKET\", \"value\": \"${S3_CSV_BUCKET}\"},
      {\"name\": \"PYTHONUNBUFFERED\", \"value\": \"1\"}
    ],
    \"logConfiguration\": {
      \"logDriver\": \"awslogs\",
      \"options\": {
        \"awslogs-group\": \"/aws/batch/job\",
        \"awslogs-region\": \"${AWS_DEFAULT_REGION}\",
        \"awslogs-stream-prefix\": \"gpu-teaching-caption-job\"
      }
    },
    \"command\": [\"python\", \"-c\", \"import torch; print(torch.cuda.is_available())\"]
  }"
```

The default command only checks that CUDA is visible. Lesson 08 replaces it with `python /app/describe_items.py` for the catalog run. Logs appear under `/aws/batch/job` only after the job reaches `STARTING` / `RUNNING` — not while it sits in `RUNNABLE`.

```bash
BATCH_JOB_DEFINITION=gpu-teaching-caption-job
```

Submit by that name. Batch uses the highest active revision. Do not submit `:1` or `:2`.
