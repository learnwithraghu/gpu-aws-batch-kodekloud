# Step 01 — Inspect the Dockerfile

Open the course `Dockerfile` at the repo root and read it together. Nothing
to execute — this step is reading.

Three things to notice:

1. **`pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime`** — Python + PyTorch +
   CUDA 11.8 for the g4dn.xlarge (NVIDIA T4).
2. **`requirements-gpu.txt`** — pinned deps (see `transformers==4.46.3` for
   torch 2.1). One `RUN pip install -r` layer caches until that file changes.
3. **`.dockerignore`** — keeps the build context to lessons + requirements only.
4. **`COPY lessons/`** — Batch selects the script at submit time via `command`.

**Expected:** you can explain what each line of the Dockerfile does.
