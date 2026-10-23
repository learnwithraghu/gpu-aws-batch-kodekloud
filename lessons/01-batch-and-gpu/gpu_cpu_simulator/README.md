# KodeFood — Sequential CPU vs Parallel GPU

Part of [Lesson 01 — AWS Batch and the GPU](../README.md) and **Section 002** (`Demo 007` / `Lab 008`).

One clear interactive demo:

**Same dish tensor. Same math. Sequential CPU cores vs parallel GPU waves.**

- Left: **Host CPU** — 4 cores, 4 blocks per tick, many sequential ticks  
- Right: **NVIDIA GPU** — Streaming Multiprocessors finish the grid in a few parallel waves  
- Compare simulated times after both runs finish  

Optional: switch **64 blocks** vs **256 blocks**, adjust speed, or **Step** the CPU tick-by-tick.

## Quick start

```bash
cd lessons/01-batch-and-gpu/gpu_cpu_simulator
bash run_simulator.sh
# open http://127.0.0.1:8080
```

Or open `index.html` directly in a browser.
