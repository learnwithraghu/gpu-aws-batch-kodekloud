# Video 004 — Networking Requirements for Batch GPU Jobs

**Section:** 006 — Building the AWS Batch GPU Infrastructure
**Lecture#:** 004
**Sheet title:** Networking Requirements for Batch GPU Jobs
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 006-004-networking-requirements-for-ba

---

Permissions answer "who is allowed?" Networking answers "can it actually reach the thing?"

You need both.

This is another place where cloud GPU jobs can confuse beginners. A workload can have the right permission to pull an image or fetch data, but still fail because the network path is missing or blocked.

That makes networking a very practical concern, not just a VPC theory topic. The machine has to reach the places that matter for startup and execution. If it cannot, the failure can look like a Batch problem or an application problem even though the real issue is connectivity.

In company environments, teams usually try to be deliberate here. Give the workload the paths it truly needs, and no more than that. Enough access to pull images, reach required storage and logging systems, and fetch any runtime dependencies that are still external. But not a wide-open design by accident.

So the useful mental model is simple: IAM opens the door in principle, and networking gives you the road in practice.

Next, we move one layer up and look at how waiting work is organized before any machine is chosen.

---

## Further reading (not spoken)

- [AWS Batch: Compute resource VPC settings](https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html) — subnets and security groups on CEs
- [Amazon ECR: Interface VPC endpoints](https://docs.aws.amazon.com/AmazonECR/latest/userguide/vpc-endpoints.html) — private pulls without a public path
- [AWS PrivateLink for S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html) — keeping S3 traffic on the AWS network
