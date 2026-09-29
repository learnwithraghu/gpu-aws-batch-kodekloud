# Video 07 — Queue and compute environment binding
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What it is.** A **job queue** is the **entry point** for submitted work. Each queue has an ordered list of **compute environment ARNs** with priorities. Batch tries to place jobs on the first healthy CE; if it cannot, it may try the next. A job submitted to **`gpu-teaching-gpu-smoke-queue-spot`** only runs on CEs **attached to that queue** — not on every GPU in your account.

**Why it exists.** Organizations separate **workload classes**: overnight ETL on cheap Spot, payroll on on-demand, experiments on a small CE with low **`maxvCpus`**. Queues let you **route** jobs without passing instance IDs at submit time — submitters say *which line* to stand in, not *which EC2* to boot.

**Example — two lanes.** **Lane A:** queue **`…-queue-spot`** → CE **`…-ce-spot`** with Spot allocation → cheaper, can wait when capacity is tight. **Lane B:** queue **`…-queue-on-demand`** → CE **`…-ce-on-demand`** → steadier, requires **G/VT on-demand quota ≥ 4** (lesson one). Draw **no crossing arrows** between lanes: submitting to Spot **never** silently uses on-demand CE capacity.

When Spot is dry, the fix is **change queue or CE strategy**, not tweak the Docker image. When on-demand jobs never start but Spot works, check **`L-DB2E81BA`** before blaming Batch.

**In this course.** Default submit uses the **Spot smoke queue**. On-demand is a **fallback after quota approval**, not automatic relief.

**Visual:** Two parallel conveyor belts from “submit-job” to different CE icons; job ID tagged with queue name.

Describe-before-create hygiene so you do not duplicate CEs — next.
