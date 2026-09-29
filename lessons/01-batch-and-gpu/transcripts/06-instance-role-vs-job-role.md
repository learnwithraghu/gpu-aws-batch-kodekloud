# Video 06 — Instance role vs job role
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What they are.**

- **Instance profile / instance role** — Credentials the **EC2 host** uses: pull images from **ECR**, send logs to **CloudWatch**, talk to ECS agent. Attached to the **machine**.
- **Job role (`jobRoleArn`)** — Credentials the **container task** uses when **your Python** calls AWS APIs — here **S3** read on photos and write on CSV. Attached to the **application process inside Docker**.

**Why two roles exist.** **Separation of duties.** The machine that downloads Docker layers should not automatically read every S3 bucket in the company. The app that reads vendor photos should not launch EC2. If one role is over-scoped, a bug or supply-chain issue in the image has smaller blast radius — standard enterprise IAM design at banks and health-tech.

**Example timeline.** Instance boots → **instance role** authenticates **`batchGetImage`** to ECR → container starts → AWS injects **job role** credentials into the task environment → **`boto3.client('s3').get_object`** evaluates **job role** policies. Missing job role: CUDA **`True`**, then **`AccessDenied`** on first photo — logs show S3, not PyTorch.

**In this course.** **`ecsInstanceRole`** on the CE; **`gpu-teaching-batch-job-role`** on the job definition. README names may differ; verify ARNs in **`describe-job-definitions`**.

**Visual:** Nested boxes — outer EC2 “instance role: ECR + logs”, inner container “job role: S3”.

Spot vs on-demand and the zero-quota trap — next.
