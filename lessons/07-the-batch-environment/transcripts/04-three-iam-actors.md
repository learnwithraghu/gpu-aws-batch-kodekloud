# Video 04 — Three IAM actors
**Type:** Theory
**Runtime target:** ~3 minutes

---

So, one Batch GPU job uses three IAM principals in the same minute, and they do not share a policy.

The first is the Batch service-linked role, AWSServiceRoleForBatch. Batch assumes it to create and scale ECS and EC2 capacity. Batch creates it the first time you make a compute environment. If create complains it is missing, call create-service-linked-role with batch.amazonaws.com once. This role does not read photos.

The second is the instance profile, ecsInstanceRole. The EC2 host assumes it to pull from ECR and write logs to CloudWatch. The managed policy is AmazonEC2ContainerServiceforEC2Role. Trust is ec2.amazonaws.com. Check it with get-instance-profile. The host does not get S3. The machine that runs Docker should not hold every bucket.

The third is the job role, gpu-teaching-batch-job-role, on the job definition as jobRoleArn. The container task assumes it. Trust is ecs-tasks.amazonaws.com. This role lists both buckets, gets objects in the images bucket, and gets and puts objects in the captions bucket. That is how describe_items.py reads photos and writes the CSV KodeFood will read. Check it with get-role. The ARN goes in .env as BATCH_JOB_ROLE_ARN. An empty job role means the GPU can start and the first S3 call still fails.

Least privilege is why there are three. The Python process does not launch EC2. The host does not put a CSV.

Failures come in three shapes. Wrong service-linked role and the compute environment goes INVALID. Read statusReason. Instance profile missing ECR rights and the pull fails in STARTING with CannotPullContainerError. Missing job role and the container starts, CUDA works, then AccessDenied on the first get. That one is expensive. The GPU meter is already running.

Walk one job. Batch scales with the service-linked role. EC2 boots with ecsInstanceRole and pulls the image. The task starts with gpu-teaching-batch-job-role. Revision three and later is where jobRoleArn is filled in. Verify with describe-job-definitions.

The template those actors run from is the job definition. Next clip reads it as a contract.
