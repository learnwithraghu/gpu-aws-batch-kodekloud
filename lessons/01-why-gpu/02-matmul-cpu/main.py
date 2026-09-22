"""
Lesson 01 · Step 02 — matmul-cpu
Time ONE matrix multiply on the CPU. This is our baseline before the GPU.

Run:  python main.py
"""
import time

import torch

SIZE = 2000

a = torch.randn(SIZE, SIZE)   # lives on the CPU
b = torch.randn(SIZE, SIZE)

torch.mm(a, b)                # warm-up — the first call allocates memory

start = time.perf_counter()
torch.mm(a, b)
elapsed_ms = (time.perf_counter() - start) * 1000

print(f"Matrix size : {SIZE} x {SIZE} on CPU")
print(f"Time        : {elapsed_ms:.1f} ms")
