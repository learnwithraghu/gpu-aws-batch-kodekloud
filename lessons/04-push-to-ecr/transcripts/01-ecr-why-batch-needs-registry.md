# Video 01 — Why ECR exists for Batch
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What ECR is.** **Amazon Elastic Container Registry** — private Docker registry in **your account and region**. Stores **layered images** addressable by URI and digest.

**Why Batch needs it.** EC2 workers **pull over HTTPS** at task start; they cannot reach your laptop daemon. No pull → no container → no job.

**Example URI shape.** `<account>.dkr.ecr.ap-northeast-1.amazonaws.com/gpu-teaching:latest`

**Visual:** Batch instance pulling layers from ECR vault.

Repo vs tag vs digest — next.
