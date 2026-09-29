# Video 02 — Prefix contract
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What must align.** **`aws s3 sync ... s3://bucket/images/sample/`** and submit override **`IMAGE_PREFIX=images/sample`** — **same string**, no trailing slash surprises consistent with code.

**Why mismatches hurt.** Photos visible in console under **`images/other/`** while job lists **`images/sample/`** → **zero rows**, fast **`SUCCEEDED`**, empty or header-only CSV.

**Example debug.** Compare sync destination vs **`describe_items` env** in submit JSON.

**Visual:** Straight line laptop folder → S3 prefix → env var → list_objects.

Supported extensions — next.
