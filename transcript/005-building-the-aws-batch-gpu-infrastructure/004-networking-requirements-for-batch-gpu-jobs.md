# Video 004 — Networking Requirements for Batch GPU Jobs

**Section:** 005 — Building the AWS Batch GPU Infrastructure
**Lecture#:** 004
**Sheet title:** Networking Requirements for Batch GPU Jobs
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 005-004-networking-requirements-for-ba

---

Roles grant permission. Networking provides the path. If a GPU instance has correct IAM but cannot pull the image or download model weights, start with its outbound network path.

Batch places instances in the VPC, subnet, and security group configured on the compute environment. Those choices are set when the environment is created. KodeFood uses a subnet in one Availability Zone and a security group that allows egress. The host must reach Amazon ECR, S3, CloudWatch Logs, and, on the first model load, Hugging Face for BLIP weights.

Think in specific egress paths. The instance needs outbound HTTPS to the required AWS APIs and registries. Without a public IP, NAT gateway, or VPC endpoints, the ECS agent cannot pull from ECR and the job never truly starts. Pull timeouts and missing logs can look like Batch failures even when the root cause is networking.

GPU jobs add model artifacts to the dependency list. If BLIP weights are not fully baked into the image, the cold start fetches them over the network. A locked-down VPC can use endpoints for S3 and ECR, plus a controlled path to any remaining model host. The goal is the least network access that still lets the workload complete.

We do not need inbound SSH for normal caption runs. Batch and the agent manage the instance. Your laptop calls the Batch and S3 APIs, while the job makes outbound connections from the VPC.

When a job cannot pull or produces no startup logs, verify reachability to ECR, S3, the model host, and CloudWatch. Next, we move one layer up to job queues and scheduling.

---

## Further reading (not spoken)

- [AWS Batch: Compute resource VPC settings](https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html) — subnets and security groups on CEs
- [Amazon ECR: Interface VPC endpoints](https://docs.aws.amazon.com/AmazonECR/latest/userguide/vpc-endpoints.html) — private pulls without a public path
- [AWS PrivateLink for S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html) — keeping S3 traffic on the AWS network
