# Video 03 — Networking for pulls and downloads
**Type:** Theory
**Runtime target:** ~3 minutes

---

Alright. When Batch launches an instance, it lands in a subnet with a route table and a security group. It may or may not have a public IP. Those choices decide whether the machine can reach ECR, S3, the internet, and CloudWatch Logs. A perfect container still dies before Python starts if the host cannot pull the image or download the model.

This course needs four outbound paths. ECR, to pull gpu-teaching tag latest. S3, to list and get photos and put the CSV. Hugging Face at huggingface.co, for the first download of caption weights. CloudWatch Logs, for stdout and stderr once the job is starting. Region stays ap-northeast-1 so the data plane matches the buckets, registry, and compute environment.

The teaching pattern is a public subnet with a public IP, so those endpoints work without private VPC endpoints. The live environments use subnet subnet-b560b3fd in ap-northeast-1a, and security group sg-bd00e4f5. That group must allow outbound HTTPS on 443. Wrong subnet or locked egress shows up as a pull timeout or model download failure, not a Python syntax error.

Memorize the failure names. Cannot pull the image and the job dies in STARTING with CannotPullContainerError. Blocked HTTPS to S3 or huggingface.co and the pull may succeed while the first model download hangs. That is routing and a firewall, not AWS being broken. A private subnet with no NAT and no VPC endpoints cannot reach the internet. A security group with no outbound HTTPS cannot either.

Large platforms often add VPC endpoints for ECR and S3. This course skips that so the first GPU job has fewer parts. Use the subnet and security group already wired into the smoke environment. KodeFood's photo check needs those four paths, not a new network design.

If describe on the compute environment says INVALID, read statusReason. Bad subnet or security group shows up there. If the environment is VALID and the job still cannot pull, check egress and routes before the caption code.

Three IAM identities act in that launch. They are next.
