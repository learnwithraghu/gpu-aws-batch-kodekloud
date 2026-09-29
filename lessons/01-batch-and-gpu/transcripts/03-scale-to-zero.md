# Video 03 — Scale to zero
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What it is.** **`minvCpus: 0`** on a managed compute environment tells Batch: **when no jobs need capacity, desired vCPUs may go to zero** — no EC2 instances required to stay running for the CE. **`maxvCpus`** still caps the burst so a runaway script cannot request a hundred GPUs.

**Why it exists.** GPU instances are **priced per second while alive**. Vendor photo drops — like menu updates for a regional restaurant chain — may arrive **hours apart**. Always-on **`g4dn`** is paying for a **standby chef** when the dining room is empty. Scale-to-zero matches **sparse batch inference** economics: spend only during the caption run.

**Example — graph narrative.** Midnight: queue empty, **desired vCPUs = 0**, spend flat. 2 p.m.: **`submit-job`**, queue depth 1, Batch raises desired toward **4 vCPUs** (one `g4dn`), instance boots, container runs, CSV written, **`SUCCEEDED`**. 2:08 p.m.: queue empty again, capacity drains to zero. Compare to a line chart of an always-on instance: flat cost 24/7.

**Tradeoff students must accept.** **Cold start** after idle: boot + ECR pull + model download (lesson eight). That latency is the **price** of zero idle GPUs — same trade Uber makes between driver supply and rider wait time.

**In this course.** CEs use **`minvCpus=0`** aligned with lesson zero’s batch-vs-always-on story.

**Visual:** Queue depth and EC2 count dual chart; dollar meter only rises when depth > 0.

GPU placement requires AMI, GPU flag, and honest memory — next.
