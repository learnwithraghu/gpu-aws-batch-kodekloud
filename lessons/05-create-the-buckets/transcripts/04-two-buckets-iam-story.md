# Video 04 — Two buckets, clearer IAM
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What we do.** **Images bucket** — vendor uploads, job reads. **CSV bucket** — job writes catalog, app reads.

**Why not one bucket.** Possible with prefixes; **two buckets** teach **least privilege** cleanly — job role read A, write B — and reduce accidental deletion of raw uploads while cleaning outputs.

**Example IAM sentence.** “Task may **GetObject** on `images/*`, **PutObject** on `descriptions/*` in CSV bucket.”

**Visual:** Two buckets; read arrow on left, write arrow on right from job role.

Prefixes and `.env` — next.
