# Video 03 — Demo: walk through photos.py
**Type:** Demo  
**Runtime target:** ~3–4 minutes

---

**Purpose.** Show students **where configuration enters** and **how S3 keys become CSV rows** — no GPU required to understand this file.

Open **`photos.py`**. Top: **`os.environ`** reads **`S3_BUCKET`**, **`S3_CSV_BUCKET`**, **`IMAGE_PREFIX`** — explain these are **injected at submit**, not secrets in Git.

**`list_photo_keys`:** prefix filter, extension filter (jpg/jpeg/png), sorted order — “inventory scan” for one vendor folder.

**`download_photo`:** **`GetObject`** bytes → Pillow RGB — CPU work before GPU.

**`save_csv`:** derive **`descriptions/<stem>/descriptions.csv`** from **`images/<stem>`**; columns **`image_s3_uri`**, **`item_description`**.

**Visual:** Highlight env vars → list → download → write path on one diagram.

Demo **`describe_items.py`** — next.
