# Video 05 — End-to-end recap
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**Full path in one breath.** **S3** photos → **Python** (I/O + GPU) → **Docker amd64** → **ECR push** → **Batch** CE/queue/job def + roles → **submit overrides** → **logs** → **CSV** → **app**.

**Next vendor checklist.** Sync **`images/<stem>/`** → submit matching **`IMAGE_PREFIX`** → **`SUCCEEDED`** → validate CSV → rebuild **only** if container changed.

**What students can now do.** Design **offline GPU batch** with scale-to-zero, diagnose **RUNNABLE**, split **IAM**, treat **CSV as product**.

**Visual:** Six-station loop diagram from lesson zero map, completed.

Demo read CSV — next.
