# Video 02 — Base image and dependency pinning
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What the base image is.** A **parent container filesystem** declared in Dockerfile **`FROM`**. Our **`pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime`** image ships **Linux**, **CUDA 11.8 runtime libraries**, and **PyTorch built against that CUDA** — the hard compatibility triangle already solved by PyTorch maintainers.

**Why start from a GPU runtime base.** Building CUDA + cuDNN + PyTorch from scratch in every project is weeks of engineering. Batch teaching needs **“add requirements + copy scripts”** — same model as starting from **`node:20`** for a web app instead of compiling Node from source.

**What we add.** **`pip install -r requirements-gpu.txt`** pins **`transformers==4.46.3`**, boto3, Pillow, etc. **`COPY`** lesson two files to **`/app`**.

**Why pin transformers.** Hugging Face libraries **move fast** and declare **minimum Torch versions**. On PyTorch 2.1, **`pip install transformers` without pin** might pull a release that **refuses to import** or disables GPU paths → container exits code 1 → no CSV. Pinning is how Pinterest-style teams **freeze** a working stack for reproducible batch jobs.

**Example failure narrative.** Student unpins for “latest features,” rebuild succeeds, push succeeds, Batch **`FAILED`** in 30 seconds with **`ImportError`** in CloudWatch — not a Batch bug.

**Visual:** Layer cake — PyTorch base (thick), pip pin (medium), your two .py files (thin).

Build context safety — next clip.
