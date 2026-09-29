# Video 02 — The four Batch objects
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What they are — four nouns every Batch diagram uses.**

1. **Compute environment (CE)** — Rules for **which EC2 capacity** Batch may create: instance types, Spot vs on-demand, VPC, **`minvCpus` / `maxvCpus`**, AMI flavor for GPUs.
2. **Job queue** — A **named pipe** jobs enter when submitted; linked to one or more CEs with priority.
3. **Job definition** — A **registered, versioned template** (not a single run): which **ECR image**, how much **CPU/memory/GPU**, which **job role** for S3/API calls inside the container, default **command**, logging. AWS stores **`name:revision`** (e.g. **`caption-job:4`**). Submit usually references the name; Batch picks the latest active revision unless you pin.
4. **Job** — **One execution** of that template: unique **job ID**, status timeline (**`SUBMITTED` → … → `SUCCEEDED`**), optional **overrides** for this run only.

**Why the split exists.** Platform teams own CEs and queues (cost, security, instance types). Application teams own job definitions and submits (business logic, env vars). Jobs are **audit units** — finance asks “how much did vendor X cost?” per job ID, not per vague cluster.

**Example — caption job in plain language.** CE: “May use Spot `g4dn.xlarge` in Tokyo, scale from zero.” Queue: “`gpu-teaching-gpu-smoke-queue-spot` uses that CE.” Job definition: “Run **`gpu-teaching:latest`**, 1 GPU, 12 GiB RAM, job role for S3, default CUDA check.” Job: “Tonight’s run for **`images/sample`** with overrides pointing **`describe_items.py`** at that prefix.”

**Metaphor.** Job definition = **recipe card** in a Chipotle back office. Job = **one burrito** made from that card. Queue = **ticket rail** when grills are busy. CE = **kitchen** that can open or close grill lines based on demand.

**Student confusion to kill early.** Changing the **Docker image for everyone** → new **job-definition revision**. Changing **only this folder’s S3 prefix** → **submit override**, not a new revision.

**Visual:** Four boxes left-to-right with one job icon spawning from definition; many job icons from one definition card.

Scale-to-zero on the compute environment — why the kitchen can close — is next.
