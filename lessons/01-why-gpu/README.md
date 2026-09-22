# Lesson 01 — Why GPU?

> **Concepts**: CPU vs GPU architecture · Parallelism · Why matrix math maps to GPUs  
> **AWS needed**: None — runs entirely on your local machine

---

## The Mental Model

Think of computation like painting a wall:

| | CPU | GPU |
|--|-----|-----|
| Workers | 8–32 very smart painters | 3,000–10,000 simple painters |
| Each worker | Can do complex decisions, branching logic | Does one thing: paint one pixel |
| Best at | Sequential tasks, complex logic (web servers, databases) | Massively parallel tasks (matrix math, pixels, image processing) |

**Machine learning is all matrix multiplication.** Training a neural network or running BLIP is basically millions of multiply-add operations happening at the same time. GPUs are designed exactly for this.

---

## What Happens in This Lesson

You'll time the same matrix multiplication on CPU and GPU using PyTorch, across three matrix sizes. You'll see the GPU go from "barely faster" (small matrices) to "dramatically faster" (large matrices).

This is the core intuition: **GPUs pay off at scale.**

---

## What is PyTorch? (30-second version)

PyTorch is a Python library for tensor math — the same math that powers neural networks. A "tensor" is just an n-dimensional array (like numpy). PyTorch can run tensor operations on CPU or GPU by moving the tensor to the right device.

```python
x = torch.randn(1000, 1000)          # lives on CPU
x = x.to("cuda")                     # moves to GPU
```

That's it. Same operations, different device, very different speed.

---

## Running the Lesson

```bash
python lessons/01-why-gpu/benchmark_gpu.py
```

(No PyTorch on your machine? `uv run --with torch python lessons/01-why-gpu/benchmark_gpu.py`)

**If you don't have a local GPU**: the script detects this automatically and falls back to reference times recorded on a g4dn.xlarge (NVIDIA T4), so you still see the full comparison. You'll get real GPU numbers in Lesson 02 when the job runs on AWS Batch.

Example output:

```
size      |  CPU (ms) |  GPU (ms) |  speedup
--------------------------------------------------
   500x500  |      4.2  |      0.8  |     5.3x
  2000x2000 |    145.7  |      8.2  |    17.8x
  5000x5000 |   3612.4  |    119.0  |    30.4x
```

---

## Key Takeaway

> A GPU is not always faster — it's faster when the work is **massively parallel**.  
> Image captioning, image classification, image generation: all massively parallel. ✅  
> Reading a CSV, running a SQL query: sequential. ❌
