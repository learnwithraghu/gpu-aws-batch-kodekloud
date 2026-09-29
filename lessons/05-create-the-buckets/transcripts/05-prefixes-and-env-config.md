# Video 05 — Prefixes and .env
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What a prefix is.** **Key prefix string** — `images/sample/` — not a true filesystem folder. S3 UI **simulates** folders by grouping on `/`.

**Why contracts use prefixes.** **`list_objects_v2(Prefix=IMAGE_PREFIX)`** defines **which photos belong to this batch job**.

**`.env` role.** Stores **bucket names** for CLI and submit env — **gitignored**. **Not** for long-lived AWS keys — use **`aws configure`** and **job role** in cloud.

**Example.** `.env` has bucket names; laptop and Batch both reference same strings, different credentials path.

Demo create buckets — next.
