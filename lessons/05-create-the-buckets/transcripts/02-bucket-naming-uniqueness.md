# Video 02 — Bucket naming
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What global uniqueness means.** S3 bucket names are **shared namespace worldwide** — first creator wins **`my-data`**.

**Why suffix with account ID.** **`gpu-teaching-images-<account-id>`** — collision-resistant, ties resource to **your** AWS account in console and IAM ARNs.

**Historical note.** CSV bucket may include **`captions`** in name; **prefix** for new data is **`descriptions/`** — do not rename live buckets mid-course.

**Visual:** `@handle` uniqueness metaphor for bucket names.

Region constraint — next.
