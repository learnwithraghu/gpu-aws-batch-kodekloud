# Video 01 — Submit vs run
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What it is.** **`aws batch submit-job`** (or the console equivalent) **accepts** a job into a **queue** and returns a **job ID**. **Running** means Batch found **capacity**, started an instance, pulled the image, and your **process is executing** inside the container.

**Why the distinction matters.** New operators treat “I got a job ID” as “the GPU is captioning now.” In reality, **acceptance is instant**; **placement is competitive** — especially for Spot **`g4dn`**. Debugging belongs in **status**, **statusReason**, and **CE desired vCPUs** until the job reaches **`STARTING`**.

**Example timeline.** T+0s: **`SUBMITTED`**. T+30s–10min: **`RUNNABLE`** while Batch searches Spot capacity or scales CE from zero. T+?: **`STARTING`** — pull image, create container. T+?: **`RUNNING`** — Python logs appear. T+end: **`SUCCEEDED`** if exit code 0.

Compare to ordering on Amazon: **order placed** ≠ **package on truck** ≠ **delivered**.

**In this course.** Most “slow” time is **`RUNNABLE`** or cold **`STARTING`**, not BLIP inference on 30 photos.

**Visual:** Timeline bar with labeled phases; highlight gap between submit and RUNNING.

Container overrides — how one template aims at different folders — next.
