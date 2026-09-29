# Video 07 — Cancel and resubmit
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What cancel does.** **`cancel-job`** stops a **queued or running** job from completing normally — with a **reason** string for audit. It does not undo S3 writes from a job that already **`SUCCEEDED`**.

**Why discipline matters.** Scenario: Spot job **`RUNNABLE`** for 20 minutes; student submits **duplicate on-demand** “to help.” Spot capacity returns — **both** may run, **double GPU cost**, **race** writing the same **`descriptions/sample/descriptions.csv`** — last writer wins, confusing debugging.

**Example playbook.**

1. One **active** attempt per vendor folder in this course.
2. **`RUNNABLE`** on Spot → wait, check quota, use watch script — do not pile on-demand unless **`L-DB2E81BA ≥ 4`** and you **cancel** the Spot attempt intentionally.
3. After fix (quota approved, prefix fixed, new image pushed) → **cancel** stale job → **one** resubmit.

**Visual:** Two job IDs converging on one S3 key — red X; single job ID — green check.

Demo: submit and watch — next.
