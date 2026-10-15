# Video 003 — IAM Roles in AWS Batch: Service, Instance and Job Roles

**Section:** 005 — Building the AWS Batch GPU Infrastructure
**Lecture#:** 003
**Sheet title:** IAM Roles in AWS Batch: Service, Instance and Job Roles
**Type:** Video
**Runtime target:** ~3 minutes
**Topic code:** 005-003-iam-roles-in-aws-batch--servic

---

IAM becomes much easier once you stop thinking about "the job" as one actor.

In reality, several different actors are involved, and each one needs a different level of permission.

There is the AWS service that manages scheduling and capacity. There is the machine that has to pull images and run containers. And there is the application workload inside the container, which needs access only to the data it is supposed to process.

That separation is not just AWS complexity for its own sake. It is how real teams reduce blast radius. You do not want every layer to have every permission. You want each layer to do only its own job.

This also makes debugging much cleaner. If the platform cannot manage capacity, that points to one kind of identity problem. If the machine cannot start the container properly, that points to another. If the application starts but cannot read or write the data it needs, that points to the workload identity.

So the real lesson here is not memorizing role names. It is learning to separate orchestrator permissions, host permissions, and application permissions.

That is a very production-oriented way to think, and it helps immediately when you see an access failure in the wild.

Next, we pair permission with connectivity and look at the network path a Batch GPU job still needs in order to work.

---

## Further reading (not spoken)

- [AWS Batch: IAM policies, roles, and permissions](https://docs.aws.amazon.com/batch/latest/userguide/IAM_policies.html) — service, instance, and job roles
- [Amazon ECS: Task IAM roles](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html) — same job-vs-instance split on ECS
- [AWS: Service-linked roles for Batch](https://docs.aws.amazon.com/batch/latest/userguide/using-service-linked-roles.html) — `AWSServiceRoleForBatch`
