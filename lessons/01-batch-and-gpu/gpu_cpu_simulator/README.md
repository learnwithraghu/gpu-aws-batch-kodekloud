# KodeFood — From Pixels to Tensors Simulator

Part of [Lesson 01 — AWS Batch and the GPU](../README.md) and **Section 002 — GPU Fundamentals: From Silicon to Cloud** (`Demo 007` and `Lab 008`).

Focused interactive lab for one teaching arc:

**From Pixels to Tensors: Sequential CPU vs Parallel GPU**

Students walk a KodeFood dish photo through four stages:

1. **What the computer sees** — toggle visual pixels / raw RGB / normalized tensor floats; click a patch to inspect `[R, G, B]` (`Shape: [3, H, W]`).
2. **Inside one layer** — step the shared multiply-and-add formula (`Output = R·wr + G·wg + B·wb + bias`) on one block or the whole grid.
3. **Sequential CPU vs parallel GPU** — step/play 4 CPU cores across the tensor; run GPU with PCIe → VRAM → parallel SM waves; compare simulated times.
4. **Scale-up** — slide from 1 photo → 30 (one vendor) → 3,000 (100 vendors) to see why GPU bursts + Batch scale-to-zero fit KodeFood.

Checkpoints unlock when you (1) inspect a patch, (2) finish a CPU run, and (3) finish a GPU run.

## Quick start

```bash
cd lessons/01-batch-and-gpu/gpu_cpu_simulator
bash run_simulator.sh
# open http://127.0.0.1:8080
```

Or open `index.html` directly in a browser (no server required).
