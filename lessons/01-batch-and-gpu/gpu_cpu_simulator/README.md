# KodeFood GPU vs CPU Interactive Simulator

Part of [Lesson 01 — AWS Batch and the GPU](../README.md) and **Section 002 — GPU Fundamentals: From Silicon to Cloud** (`Demo 007` and `Lab 008`).

This zero-dependency HTML/CSS/JS learning app lets students interact with three hands-on missions before building the Docker container in Section 003:

1. **Mission 1 — Pixel & Tensor Matrix Race:** Compare 4 fast sequential CPU cores against thousands of parallel GPU threads on a 64-block dish image tensor.
2. **Mission 2 — CPU vs GPU Task Router:** Route the 6 real KodeFood pipeline steps (`photos.py` S3 I/O, JPEG decode, and CSV upload vs `describe_items.py` BLIP vision and token layers) to the right processor.
3. **Mission 3 — Inside `g4dn.xlarge`: VRAM & Micro-Batch Tuner:** Tune `BATCH_SIZE` (`1`, `4`, `8`, `16`, `30`) against a 16 GB NVIDIA T4 GPU and 16 GB Host RAM to witness a CUDA Out-of-Memory (`OOM`) crash at `BATCH_SIZE=30` and find the optimal `BATCH_SIZE=8` profile.

## Quick start (local browser or HTTP server)

Option A — Run the lightweight local server:

```bash
cd lessons/01-batch-and-gpu/gpu_cpu_simulator
bash run_simulator.sh
# open http://127.0.0.1:8080
```

Option B — Open directly in any browser (no server needed):

```bash
open lessons/01-batch-and-gpu/gpu_cpu_simulator/index.html
```
