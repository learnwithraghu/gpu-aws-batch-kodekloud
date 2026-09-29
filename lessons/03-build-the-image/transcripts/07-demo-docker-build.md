# Video 07 — Demo: docker build
**Type:** Demo  
**Runtime target:** ~3–4 minutes

---

**Purpose.** Produce **`gpu-teaching:latest`** locally with the **correct platform** for Batch.

Docker Desktop running; repo root. Run **`docker build --platform linux/amd64 -t gpu-teaching:latest .`**. Narrate layers: base, pip pin **`transformers`**, COPY **`photos.py`** / **`describe_items.py`**.

First build: set **15–25 min** expectation. Finish with **`docker images`**.

**Segue:** lesson four **push** — Batch only pulls from ECR.
