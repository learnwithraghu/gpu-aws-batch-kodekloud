# Video 04 — Stuck in RUNNABLE
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What it means.** **`RUNNABLE`** = “Batch knows about your job and **could** run it, but **has not** placed it on a started task yet.” It is **not** “Python is slow.”

**Why students misdiagnose it.** They open **`/aws/batch/job`** — **empty** — and edit **`describe_items.py`**. But **no container ⇒ no stdout**. Logs appear only after **`STARTING`** succeeds.

**Checklist — cause → signal.**

1. **Spot capacity dry** — Spot queue, long RUNNABLE, **`statusReason`** mentions capacity; CE **`desiredvCpus`** may stay 0 or rise slowly.
2. **On-demand quota zero** — on-demand queue, **`L-DB2E81BA = 0`**, never launches regardless of “healthy” CE.
3. **Memory misconfiguration** — e.g. **16384 MiB** on `g4dn` → **`MISCONFIGURATION:JOB_RESOURCE_REQUIREMENT`** in reason; never RUNNING.
4. **CE INVALID/disabled** or queue points at wrong CE — describe APIs show red status.
5. **Wrong region/account** — job in Tokyo, CE in Oregon — rare but catastrophic.

**Example command habit.** **`aws batch describe-jobs --jobs $JOB_ID`** — read **`statusReason`**, **`container.logStreamName`** (may be null while RUNNABLE).

**In this course.** Prefer **Spot**; use **`watch_batch_job.sh`** for quota hint after ~2 minutes.

**Visual:** RUNNABLE job with “no log stream yet” badge; decision tree of five checks.

Quotas and cold-start slowness after placement — next.
