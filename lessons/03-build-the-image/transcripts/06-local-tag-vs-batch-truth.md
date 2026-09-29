# Video 06 — Local tag vs what Batch runs
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What `docker images` shows.** Local tags on **your machine** — not visible to AWS until **push**.

**Why two truths confuse teams.** “I built today” vs “ECR **latest** still yesterday” → stale captions.

**Example workflow truth table.** Build only → Batch unchanged. Build + push → Batch picks new digest on **`latest`**.

**Visual:** Broken bridge until push connects laptop to ECR.

Demo **`docker build`** — next.
