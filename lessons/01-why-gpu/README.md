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
| Best at | Sequential tasks, complex logic (web servers, databases) | Massively parallel tasks (matrix math, pixels, embeddings) |

**Machine learning is all matrix multiplication.** Training a neural network or running CLIP is basically millions of multiply-add operations happening at the same time. GPUs are designed exactly for this.

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

Open `notebook.ipynb` and run all cells top-to-bottom.

**If you don't have a local GPU**: The GPU cells will be skipped automatically. Pre-saved benchmark results are shown so you still see the comparison. You'll get to see real GPU numbers in Lesson 02 when the job runs on AWS Batch.

---

## Key Takeaway

> A GPU is not always faster — it's faster when the work is **massively parallel**.  
> Image captioning, image classification, text embedding: all massively parallel. ✅  
> Reading a CSV, running a SQL query: sequential. ❌
