# Video 04 — Three IAM actors
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What it is.** **IAM roles** are temporary credentials **AWS services or EC2 assume** to call other AWS APIs. In a Batch GPU job, **three different principals** act, often in the same minute:

1. **AWS Batch service-linked role** (`AWSServiceRoleForBatch`) — Batch itself assuming permission to **create and manage ECS/EC2 capacity** on your behalf.
2. **EC2 instance profile** (here **`ecsInstanceRole`**) — the **host** assuming permission to **pull from ECR** and **write container logs** to CloudWatch.
3. **Job role** (here **`gpu-teaching-batch-job-role`**, via **`jobRoleArn`**) — the **container task** assuming permission to **read and write S3** for catalog I/O.

**Why it exists.** **Least privilege.** The host that runs Docker should not automatically get blanket S3 access to every bucket in the account; the Python process should not need permissions to launch EC2. Splitting roles limits blast radius when code is wrong or compromised — the same reason Google Cloud separates service account per microservice.

**Example — failure stories students recognize.** **Wrong or missing service-linked role:** compute environment goes **`INVALID`**, nothing scales. **Instance profile missing ECR rights:** image pull fails in **`STARTING`**, logs mention **`CannotPullContainerError`**. **Job definition missing job role:** container starts, CUDA works, first **`s3.get_object`** throws **`AccessDenied`** — expensive failure because the GPU minute meter already ran.

Walk through one job timeline on screen: Batch service scales CE → EC2 boots with **instance profile** → agent pulls image → task starts with **job role** → **`describe_items.py`** reads photos. Three badges, three arrows, never swapped.

**In this course.** Lesson seven registers **`jobRoleArn`** on the job definition (revision three and above in the teaching story). Lesson one introduced the idea; here it becomes a field you must verify in **`describe-job-definitions`**.

**Visual:** Org chart — “Batch service”, “EC2 host”, “Container task” with separate policy attachments (ECR/logs vs S3).

The template those tasks run from — fields and meaning — we unpack fully in the job definition clip you just heard referenced; next, revision history.
