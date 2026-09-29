# Video 03 — Networking for pulls and downloads
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What it is.** **VPC networking** for Batch means: when an EC2 instance launches for your job, it lands in a **subnet** with a **route table**, **security groups**, and optionally a **public or private IP**. Those choices decide whether the instance can reach **ECR**, **S3**, the **internet** (for Hugging Face model downloads), and **CloudWatch Logs**.

**Why it exists.** A perfectly built job definition fails in **`STARTING`** if the instance cannot pull the image — `CannotPullContainerError` — or if HTTPS to S3 or `huggingface.co` is blocked. These failures look like “AWS is broken” to beginners but are **routing and firewall** problems: no NAT gateway in a private subnet, wrong security group egress, NACL denying outbound TLS.

**Example — this course’s teaching pattern.** Instances in a **public subnet** with **assign public IP** can reach AWS endpoints and the public internet directly. Security group allows **outbound** traffic needed for HTTPS (443). On screen, draw the instance with arrows: **ECR** (image layers), **S3** (photos and CSV), **huggingface.co** (first-run weight download), **logs.** Region stays **`ap-northeast-1`** so none of these arrows cross the Pacific for data plane work.

**Enterprise contrast (one sentence).** Netflix-scale setups often use **VPC interface endpoints** for ECR and S3 so traffic never leaves the Amazon network; that saves NAT cost and tightens security. We skip that complexity so the first GPU job succeeds with fewer moving parts.

**In this course.** Lesson docs reference an existing VPC, subnet, and security group wired into the smoke compute environment. Your account may differ; the **invariant** is: from a Batch instance, prove **curl/https** paths to ECR and S3 work before debugging Python.

**Visual:** Map pin Tokyo; instance bubble; four outbound arrows with service icons. Red X variant: “private subnet, no NAT, no endpoints” with pull timeout message.

Three different IAM identities participate in the same launch — next.
