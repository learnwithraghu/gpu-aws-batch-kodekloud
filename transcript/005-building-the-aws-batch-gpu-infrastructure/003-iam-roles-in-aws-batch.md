# Video 003 — IAM Roles in AWS Batch: Service, Instance and Job Roles

**Section:** 005 — Building the AWS Batch GPU Infrastructure
**Lecture#:** 003
**Sheet title:** IAM Roles in AWS Batch: Service, Instance and Job Roles
**Type:** Video
**Runtime target:** ~3 minutes
**Topic code:** 005-003-iam-roles-in-aws-batch--servic

---

Drivers get the GPU working. IAM decides who is allowed to touch what. In Batch you do not have one role. You have three actors, and mixing them up is the fastest way to get a confusing AccessDenied.

First, the Batch service role — typically the service-linked role `AWSServiceRoleForBatch`. This is Batch itself managing compute environments: creating ECS clusters, scaling EC2, attaching capacity. If this role is wrong, environments never become healthy. You will not get as far as a caption container.

Second, the instance role, attached through an instance profile — in our account that is `ecsInstanceRole`. The EC2 host and the ECS agent use it. They need to pull the image from Amazon ECR and write container logs to CloudWatch. They do not need permission to read vendor photos or write `descriptions.csv`. Keep that narrow. The instance role is about running containers, not about your business data.

Third, the job role — set as `jobRoleArn` on the job definition. The container assumes this role while `describe_items.py` runs. For KodeFood that role lists and reads the images bucket and writes the catalog CSV bucket. Without it, the instance can pull ECR just fine and the job still dies on S3 AccessDenied the moment photos.py lists a prefix.

Why three roles instead of one fat role on the instance? Least privilege and blast radius. If every container inherited full S3 power from the instance profile, any job definition mistake becomes a data-plane incident. Separating job credentials is the same idea Amazon documents for ECS task roles: the task gets application permissions; the instance gets agent permissions.

You will see this split in production Batch shops and in ECS services alike. Different teams name it “platform role” versus “job role,” but the shape is the same: orchestrator, host, workload.

For this course, remember the failure map. Environment stuck invalid — check the service role. Image pull or log failures at STARTING — check the instance role. AccessDenied inside the Python process — check the job role on the active job-definition revision. When you re-register a definition, confirm the new revision still carries `jobRoleArn`; silent omissions recreate last month’s bug.

That’s the IAM triangle. Next we put the instance on a network path that can actually reach ECR, S3, Hugging Face for the model, and CloudWatch Logs.

---

## Further reading (not spoken)

- [AWS Batch: IAM policies, roles, and permissions](https://docs.aws.amazon.com/batch/latest/userguide/IAM_policies.html) — service, instance, and job roles
- [Amazon ECS: Task IAM roles](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html) — same job-vs-instance split on ECS
- [AWS: Service-linked roles for Batch](https://docs.aws.amazon.com/batch/latest/userguide/using-service-linked-roles.html) — `AWSServiceRoleForBatch`
