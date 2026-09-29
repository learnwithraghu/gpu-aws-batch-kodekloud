# Video 05 — The catalog file and the AWS map
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What the product is.** Rows in **`descriptions.csv`**: **`image_s3_uri`**, **`item_description`**. The food app **reads this file**; it does not re-run BLIP at request time for this offline pipeline.

**Why offline generation.** Captioning is **expensive and slow** relative to HTTP; precomputing catalog text keeps app loads fast and decouples ML releases from mobile deploys — same pattern as pre-rendered thumbnails on YouTube.

**Three AWS roles — what / why / holds.**

| Service | What it is | Why in pipeline | Holds |
|---------|------------|-----------------|--------|
| **S3** | Object storage | Durable I/O across ephemeral GPUs | Photos + CSV |
| **ECR** | Private Docker registry | Instances pull your pinned stack | Image with CUDA + code |
| **Batch** | Job scheduler | Scale GPU runs without 24/7 box | Runs container to completion |

**Example flow sentence.** Sync photos to S3 → build/push image to ECR → Batch job pulls image, reads S3, writes CSV → app reads CSV.

Lesson one zooms into **Batch objects** (queue, definition, job). Lesson two writes the **Python** Batch will run.

**Visual:** Three pillars S3 / ECR / Batch with arrows; app reads only S3 CSV.
