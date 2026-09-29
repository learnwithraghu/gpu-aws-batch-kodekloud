# Video 02 — I/O file vs GPU file
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What it is.** **`photos.py`** — **I/O layer**: S3 list/download, image decode helpers, CSV write. **`describe_items.py`** — **compute layer**: load BLIP, run **`generate`**, orchestrate batches, call **`photos.py`**.

**Why split modules.** Different failure modes: **`AccessDenied`** vs **`CUDA False`** vs bad prompt. Different skills on teams: data engineering vs ML. One **process** still — Batch runs **`describe_items.py`**, which **imports** **`photos.py`**.

**Example call chain.** `main()` → list keys for **`IMAGE_PREFIX`** → loop batches → download each image → GPU caption → accumulate strings → **`save_csv`** once.

**Industry parallel.** Instacart-style pipelines separate **warehouse scanning** from **ranking model**; same job ID, different files to open in an incident.

**Visual:** Two modules; one OS process bubble around both.

Demo walk **`photos.py`** — next.
