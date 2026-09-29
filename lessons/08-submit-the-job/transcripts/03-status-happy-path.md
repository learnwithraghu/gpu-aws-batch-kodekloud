# Video 03 — Status happy path
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What it is.** Batch exposes a **job status** string updated as the control plane and ECS move the job forward. Status is the **first screen** in ops — before logs, before S3.

**Why each state exists.**

- **`SUBMITTED`** — Record created; validation passed.
- **`RUNNABLE`** — Eligible to run; waiting for **scheduler placement** or capacity.
- **`STARTING`** — Instance selected; **image pull**, container create, task launch.
- **`RUNNING`** — User process executing (`describe_items.py`).
- **`SUCCEEDED` / `FAILED`** — Container **exited**; Batch recorded exit code.

**Example happy path animation.** Queue → CE scales → **`STARTING`** (pull **`gpu-teaching:latest`**) → **`RUNNING`** (log lines: loading BLIP, batch 1/4) → **`SUCCEEDED`**.

**Critical nuance.** **`SUCCEEDED`** means **the container exited zero** — the process believed it finished. Lesson nine still verifies **S3**: correct key, row count, sane columns. Scheduler success ≠ product success if the app wrote nothing or wrong prefix.

**Visual:** State machine diagram with green path; side note “SUCCEEDED → still check CSV”.

Long RUNNABLE without logs — diagnosis clip next.
