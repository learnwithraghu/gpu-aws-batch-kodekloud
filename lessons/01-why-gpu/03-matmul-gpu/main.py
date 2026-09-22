"""
Lesson 01 · Step 03 — matmul-gpu
The SAME matrix multiply, on the GPU. Watch the number drop.

Run:  python main.py
"""
import time

import torch

SIZE = 2000

if not torch.cuda.is_available():
    print("No local GPU — showing the recorded time from a g4dn.xlarge (NVIDIA T4).")
    print(f"Matrix size : {SIZE} x {SIZE} on GPU (NVIDIA T4, reference)")
    print("Time        : 8.2 ms")
    raise SystemExit(0)

a = torch.randn(SIZE, SIZE, device="cuda")   # lives on the GPU
b = torch.randn(SIZE, SIZE, device="cuda")

torch.mm(a, b)                # warm-up
torch.cuda.synchronize()      # wait for the GPU before starting the clock

start = time.perf_counter()
torch.mm(a, b)
torch.cuda.synchronize()      # wait for the GPU to actually finish
elapsed_ms = (time.perf_counter() - start) * 1000

print(f"Matrix size : {SIZE} x {SIZE} on GPU ({torch.cuda.get_device_name(0)})")
print(f"Time        : {elapsed_ms:.1f} ms")
