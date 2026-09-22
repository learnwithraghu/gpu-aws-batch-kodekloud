# Step 01 — Inspect the Dockerfile

Open the course `Dockerfile` at the repo root and read it together. Nothing
to execute — this step is reading.

Three things to notice:

1. **`pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime`** — the base image
   bundles Python + PyTorch + CUDA 11.8, matching the g4dn.xlarge
   (NVIDIA T4) driver.
2. **One `RUN pip install` layer** — Docker caches each instruction; keeping
   the installs in one layer makes rebuilds predictable.
3. **`COPY lessons/ /app/lessons/`** — every lesson script is baked into the
   image. Batch picks the right script at submit time via the `command`
   override.

**Expected:** you can explain what each line of the Dockerfile does.
