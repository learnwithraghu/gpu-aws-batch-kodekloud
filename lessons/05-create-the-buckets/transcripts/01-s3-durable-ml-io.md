# Video 01 — S3 for ML input and output
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What S3 is.** **Simple Storage Service** — durable **object** store (key + bytes + metadata), 11-nines design goal, regional, accessed via HTTPS APIs (`GetObject`, `PutObject`, `ListObjectsV2`).

**Why GPU jobs need it.** Batch instances are **ephemeral** — disk gone when scaled in. Photos and CSV must **outlive** any one EC2. S3 is the **system of record** for inputs and catalog output.

**Example workflow.** Job lists **`s3://images-bucket/images/sample/`** → downloads each object → writes **`s3://csv-bucket/descriptions/sample/descriptions.csv`**. Next job may land on a **different instance**; same S3 paths work.

**Contrast local disk.** Writing CSV only on container disk → lost at exit — failure for product.

**Visual:** Ephemeral EC2 bubble; permanent S3 cylinder; arrows in/out.

Bucket naming — next.
