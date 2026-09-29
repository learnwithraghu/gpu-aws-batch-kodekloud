# Video 09 — Demo: Batch environment setup
**Type:** Demo  
**Runtime target:** ~3–4 minutes

---

**Why we’re doing this.** Students have an ECR image and S3 photos, but Batch still needs three **registered resources** — compute environment, queue, job definition — before **`submit-job`** does anything useful. This demo shows **inspect first, create only if missing**, and what “healthy” looks like in CLI output.

Source **`.env`** and set **`AWS_DEFAULT_REGION=ap-northeast-1`**. Narrate each step’s **purpose**, not only the command.

**Step 1 — Compute environment.** Run **`describe-compute-environments`** filtered to the Spot CE name from the README. If **`status` is `VALID`**, show **`computeResources.maxvCpus`**, **`minvCpus`**, and **`instanceTypes`** on screen — confirm **`g4dn.xlarge`** and **`minvCpus: 0`**. If missing, run create with **`ECS_AL2023_NVIDIA`**, VPC/subnet/security group from course docs; pause on **`imageType`** so viewers see the NVIDIA AMI choice.

**Step 2 — Queue.** **`describe-job-queues`**. Show **`state: ENABLED`** and **`computeEnvironmentOrder`** pointing at that CE ARN — verbalize: “jobs on this queue only run on that pool.”

**Step 3 — Job definition.** **`describe-job-definitions`** for **`gpu-teaching-caption-job`**. Expand **`containerProperties`**: ECR **`image`**, **`memory` 12288**, **`resourceRequirements` type GPU value 1**, non-empty **`jobRoleArn`**, **`logConfiguration`** to **`awslogs`**. Compare to the “contract” theory clip — this is that card in JSON form. If registering, show **`register-job-definition`** once and note the **new revision number**.

**Close.** Three green checks: CE **`VALID`**, queue **`ENABLED`**, job def **active revision with GPU + role**. Segue: lesson eight **`submit-job`** with **container overrides** supplies the vendor folder; the template you just verified supplies the machine shape.
