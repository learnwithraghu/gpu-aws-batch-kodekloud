# Video 02 — Container overrides
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What they are.** **Container overrides** are **per-submit** patches to the job definition’s container spec. They let this **one job** use a different **command** and **environment variables** without registering a new revision. In the API they live under **`containerOverrides`** on **`submit-job`**.

**Why they exist.** The same Docker image serves **many vendor folders**. Rebuilding or re-registering the job definition for every **`IMAGE_PREFIX`** would be slow and error-prone. Overrides are how Batch separates **platform template** (image, GPU, memory, role) from **run parameters** (which S3 prefix, which buckets, batch size).

**Example — read the JSON aloud for Remotion.** For vendor **`sample`**:

- **`command`**: `["python", "/app/describe_items.py"]` — replaces the default CUDA smoke command from lab setup.
- **`environment`**: an array of name/value pairs:
  - **`S3_BUCKET`** → images bucket name from `.env`
  - **`S3_CSV_BUCKET`** → CSV bucket name
  - **`IMAGE_PREFIX`** → **`images/sample`** — must match lesson six sync path
  - **`BATCH_SIZE`** → **`8`** — photos per GPU micro-batch

Another submit only changes **`IMAGE_PREFIX`** to **`images/vendor-b`** and the **job name** — same image, same definition revision.

**What overrides cannot fix.** Wrong **memory**, missing **GPU**, bad **image URI**, missing **jobRoleArn** — those live in the **job definition**; patch the definition and register a **new revision**.

**Visual:** Job definition card static; floating “override sticky” on command + env; two submit arrows with different IMAGE_PREFIX values.

Status progression from SUBMITTED to SUCCEEDED — next.
