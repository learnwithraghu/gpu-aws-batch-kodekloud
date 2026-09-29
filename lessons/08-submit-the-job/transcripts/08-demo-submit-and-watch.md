# Video 08 — Demo: submit and watch
**Type:** Demo  
**Runtime target:** ~3–4 minutes

---

**Purpose.** Tie together **job definition template** + **container overrides** + **queue** into one **`jobId`**, then read **status** until **`SUCCEEDED`** or a actionable failure.

Source **`.env`**. Confirm **`BATCH_JOB_QUEUE`** is the **Spot** smoke queue and **`BATCH_JOB_DEFINITION`** names **`gpu-teaching-caption-job`**.

On screen, run **`submit-job`** with **`containerOverrides`**: **`command`** → **`python /app/describe_items.py`**; **environment** → both bucket vars, **`IMAGE_PREFIX=images/sample`**, **`BATCH_SIZE=8`**. Capture **`jobId`**.

Run **`helpers/watch_batch_job.sh`**. Narrate each status change. If **`RUNNABLE`**, read any **quota** output — connect to lesson one theory.

On **`SUCCEEDED`**, pause: proof is **`descriptions/sample/descriptions.csv`** in S3, lesson nine.

**Visual:** Terminal + small status timeline graphic updating live.

Demo: **`describe-jobs`** and log stream — next.
