# Video 03 — Networking for pulls and downloads
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

When Batch launches an instance for your job, that instance lands in a subnet. The subnet has a route table. The instance has a security group. It may or may not have a public IP. Those choices decide whether the machine can reach ECR, S3, the public internet, and CloudWatch Logs. The container can be perfect and still die before your Python starts, because the host cannot pull the image or cannot download the model.

This course needs four outbound paths. ECR, so the host can pull gpu-teaching, tag latest, the image from lesson four. S3, so the job can list and get the photos, and put the CSV. Hugging Face, at huggingface.co, so the first run inside the container can download the caption model weights. CloudWatch Logs, so stdout and stderr have somewhere to land once the job is actually starting. The region stays ap-northeast-1, Tokyo, so that data plane work stays in the same region as the buckets, the registry, and the compute environment.

The teaching pattern is a public subnet, with a public IP on the instance, so those endpoints are reachable without private VPC endpoints. The live environments already use subnet subnet-b560b3fd, in availability zone ap-northeast-1a, and security group sg-bd00e4f5. The security group has to allow the outbound traffic the job needs, HTTPS on port 443 toward those services. A wrong subnet or locked-down egress shows up as a pull timeout or a model download failure. It does not show up as a Python syntax error.

The failure names are worth memorizing. If the instance cannot pull the image, the job dies in STARTING with CannotPullContainerError. If HTTPS to S3 or to huggingface.co is blocked, the pull may succeed and the first model download still hangs or fails. Beginners read that as AWS is broken. It is routing and a firewall. A private subnet with no NAT gateway and no VPC endpoints cannot reach the internet. A security group with no outbound HTTPS cannot either. A network ACL that denies outbound TLS fails the same way, one layer lower, and it is easy to miss because the security group looks open.

Large platforms often put interface endpoints in the VPC for ECR and S3, so that traffic never leaves the Amazon network. That saves NAT cost and tightens the path. This course skips that complexity so the first GPU job has fewer moving parts. Do not add a private-only design in the middle of the lab and then debug the container. Use the subnet and security group already wired into the smoke environment.

Before you debug Python, prove the path. From a Batch instance, ECR and S3 have to answer on HTTPS. If describe on the compute environment says INVALID, read statusReason. A bad subnet or security group shows up there, and the pool never becomes a place you can submit work. If the environment is VALID and the job still cannot pull, the security group egress and the route are the next read, not the caption code.

On the screen, a map pin on Tokyo, then one instance bubble. Four arrows leave it, labeled ECR, S3, huggingface.co, and logs. A second frame draws a red X on a private subnet with no NAT and no endpoints, and the caption on that frame is the pull timeout.

Three different IAM identities act in that same launch. They are next, and they are not interchangeable.
