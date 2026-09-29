# Video 03 — Row count sanity check
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What to compare.** Data rows in CSV (= **`wc -l` minus header**) vs count of **supported** image keys under prefix.

**Why it catches bugs.** Skipped extensions, wrong prefix, partial logic errors — before merchandisers trust captions.

**Example.** 30 ls keys, 28 rows → hunt **`.heic`** or list prefix typo.

**Visual:** Two numbers must match with equals sign.

When to rebuild / re-upload / resubmit — next.
