# Video 04 — Environment variables as job config
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What they are.** **Environment variables** are key/value strings injected into the container OS environment — **`os.environ`** in Python — without rebuilding the image.

**Why not hard-code buckets/prefixes.** Accounts and vendor folders differ; **twelve-factor** style keeps **one image artifact**, many runs. Same pattern as **`DATABASE_URL`** at Heroku or **`KUBERNETES_SERVICE_HOST`** in pods.

**Example overrides (lesson eight).** **`S3_BUCKET`**, **`S3_CSV_BUCKET`**, **`IMAGE_PREFIX=images/sample`**, **`BATCH_SIZE=8`**. Change prefix for **`vendor-b`** only — image unchanged.

**`BATCH_SIZE`:** count of photos per GPU forward pass — memory knob, not “number of output files.”

**Visual:** One Docker image icon; multiple env sticky notes pointing at it.

Demo GPU file — next.
