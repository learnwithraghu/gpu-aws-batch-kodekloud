# Video 004 — Networking Requirements for Batch GPU Jobs

**Section:** 005 — Building the AWS Batch GPU Infrastructure
**Lecture#:** 004
**Sheet title:** Networking Requirements for Batch GPU Jobs
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 005-004-networking-requirements-for-ba

---

Roles grant permission. Networking grants a path. A GPU instance with perfect IAM still fails if it cannot leave the subnet to pull your image or download model weights.

Batch places instances into the VPC, subnet, and security group you configure on the compute environment. Those choices are baked in when the environment is created. For KodeFood, that is a subnet in one Availability Zone and a security group that allows egress so the host can reach Amazon ECR, S3, CloudWatch Logs, and — on first model load — Hugging Face for BLIP weights.

Think in egress paths, not in “open the internet casually.” The instance needs outbound HTTPS to AWS APIs and registries. Without a public IP, NAT gateway, or VPC endpoints, the ECS agent cannot pull from ECR and your job never truly starts. With egress blocked, you get pull timeouts and missing logs that look like Batch problems but are network problems.

GPU jobs add one more dependency: model artifacts. Our image may still fetch BLIP weights on cold start if they are not fully baked in. That download needs outbound reachability too. Teams that lock down production VPCs solve this with VPC endpoints for S3 and ECR, plus a controlled path for any remaining model host — least network access that still lets the workload complete.

Notice what you do not need for this course: inbound SSH for day-to-day caption runs. Batch and the agent manage the instance. Your laptop talks to the Batch and S3 APIs; the job talks out from the VPC.

That's it here for networking: reach ECR, S3, models, and logs, or a perfect job definition still dies silent. Next — job queues and how Batch schedules across them.

---

## Further reading (not spoken)

- [AWS Batch: Compute resource VPC settings](https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html) — subnets and security groups on CEs
- [Amazon ECR: Interface VPC endpoints](https://docs.aws.amazon.com/AmazonECR/latest/userguide/vpc-endpoints.html) — private pulls without a public path
- [AWS PrivateLink for S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html) — keeping S3 traffic on the AWS network
