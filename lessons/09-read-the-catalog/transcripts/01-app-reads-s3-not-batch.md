# Video 01 — The app reads S3, not Batch
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What downstream consumes.** **`descriptions/<batch>/descriptions.csv`** in the CSV bucket — not Batch **job APIs**.

**Why separate worker from app.** Mobile/web apps should not need **IAM to SubmitJob** or poll **`RUNNABLE`**. They need a **stable artifact** — same decoupling as reading a nightly export from Snowflake instead of the warehouse query engine.

**Example failure.** Job **`SUCCEEDED`** on **`images/wrong-stem`** while app reads **`descriptions/sample/`** — empty menu, “Batch green.”

**Visual:** Batch → S3 only; App → S3 direct.

CSV as interface — next.
