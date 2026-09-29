# Video 09 — Demo: logs via describe-jobs
**Type:** Demo  
**Runtime target:** ~3–4 minutes

---

**Purpose.** Teach the **ops loop**: job ID → **metadata** → **log stream** → **actionable line**.

**`aws batch describe-jobs --jobs $JOB_ID`** — query **`status`**, **`statusReason`**, **`attempts[0].container.logStreamName`**, exit code if failed.

Open **CloudWatch** **`/aws/batch/job`**, paste stream name. On success, scroll: model load, listing keys, batch progress, CSV write. On failure (or archived example), show one **`AccessDenied`** or **`CUDA`** line and name the fix layer.

Reinforce: **`RUNNABLE`** jobs often have **null** log stream — not a logging bug.

Close the lesson arc: Batch’s job is **orchestration**; the **CSV** is the product — lesson nine reads it like the mobile app would.
