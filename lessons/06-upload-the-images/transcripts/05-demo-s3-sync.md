# Video 05 — Demo: sync photos to S3
**Type:** Demo  
**Runtime target:** ~3–4 minutes

---

**Purpose.** Put **real vendor-style photos** at the prefix jobs will list.

Local sample folder → **`aws s3 sync`** with image includes → **`s3://$S3_BUCKET/images/sample/`**. **`aws s3 ls`** count ~25–30. Console folder view matches **`IMAGE_PREFIX`**.

Emphasize: **no Docker rebuild** — data change only.

**Segue:** lesson seven Batch environment.
