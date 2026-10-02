# Video 003 — IAM Roles in AWS Batch: Service, Instance and Job Roles

**Section:** 005 — Building the AWS Batch GPU Infrastructure
**Lecture#:** 003
**Sheet title:** IAM Roles in AWS Batch: Service, Instance and Job Roles
**Type:** Video
**Runtime target:** ~3 minutes
**Topic code:** 005-003-iam-roles-in-aws-batch--servic

---

Drivers make the GPU usable. IAM decides which actor may do which work. Batch has three relevant roles, and an `AccessDenied` becomes much easier to diagnose once you identify the actor that failed.

First is the Batch service role, typically the service-linked role `AWSServiceRoleForBatch`. Batch uses it to manage compute environments, create ECS clusters, scale EC2, and attach capacity. If this role is wrong, the environment does not become healthy. The caption container never gets a chance to start.

Second is the instance role, attached through an instance profile. In our account, that is `ecsInstanceRole`. The EC2 host and ECS agent use it to pull the image from Amazon ECR and write container logs to CloudWatch. They do not need permission to read vendor photos or write `descriptions.csv`. This role runs containers; it does not grant access to the workload data.

Third is the job role, set as `jobRoleArn` on the job definition. The container assumes `gpu-teaching-batch-job-role` while `describe_items.py` runs. That role lists and reads the images bucket and writes the catalog CSV bucket. Without it, the host can pull from ECR, but the process fails with S3 `AccessDenied` when `photos.py` lists the prefix.

The separation limits privilege and blast radius. The workload receives application permissions through the job role. The host receives agent permissions through the instance role. We do not give every container broad S3 access through the instance profile.

Use the symptom to choose the check. An environment stuck `INVALID` points to the service role. Image-pull or logging failures around `STARTING` point to the instance role. An `AccessDenied` inside Python points to the job role on the active job-definition revision. After re-registering a definition, confirm that the new revision still carries `jobRoleArn`.

Those three roles cover orchestrator, host, and workload. Next, we verify that the host has a network path to ECR, S3, Hugging Face, and CloudWatch Logs.

---

## Further reading (not spoken)

- [AWS Batch: IAM policies, roles, and permissions](https://docs.aws.amazon.com/batch/latest/userguide/IAM_policies.html) — service, instance, and job roles
- [Amazon ECS: Task IAM roles](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html) — same job-vs-instance split on ECS
- [AWS: Service-linked roles for Batch](https://docs.aws.amazon.com/batch/latest/userguide/using-service-linked-roles.html) — `AWSServiceRoleForBatch`
