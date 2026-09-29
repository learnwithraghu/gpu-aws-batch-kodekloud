# Video 08 — Idempotent CSV output
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What it is.** Output key **deterministic** from input prefix: **`images/sample`** → **`descriptions/sample/descriptions.csv`**. Re-run **overwrites** same object — **latest successful run wins**.

**Why.** Ops and apps watch **one path per vendor**; no **`catalog_v3_final.csv`** sprawl. Failed mid-run should not publish partial CSV in this design — write after full pass.

**Example.** Fix prompt → rebuild image → resubmit same prefix → new descriptions replace old at **same URI**.

Lesson three packages this program into Docker.

**Visual:** Two submit arrows → one S3 key, second replaces content.
