"""
Lesson 01 · Step 04 — cpu-vs-gpu
Compare CPU and GPU across three matrix sizes and print the speedup table.

Run:  python main.py
"""
import time

import torch


def time_matmul(size, device, runs=5):
    """Time a matrix multiply of shape (size x size). Returns average ms."""
    a = torch.randn(size, size, device=device)
    b = torch.randn(size, size, device=device)

    torch.mm(a, b)                      # warm-up
    if device == "cuda":
        torch.cuda.synchronize()

    start = time.perf_counter()
    for _ in range(runs):
        torch.mm(a, b)
        if device == "cuda":
            torch.cuda.synchronize()
    return (time.perf_counter() - start) / runs * 1000


def main():
    print(f"GPU available : {torch.cuda.is_available()}\n")

    # Reference times (ms) recorded on a g4dn.xlarge (NVIDIA T4).
    # Used only when no local GPU is present.
    reference_gpu_ms = {500: 0.8, 2000: 8.2, 5000: 119.0}

    print(f"{'size':>12} | {'CPU (ms)':>9} | {'GPU (ms)':>9} | {'speedup':>8}")
    print("-" * 50)

    for size in [500, 2000, 5000]:
        cpu_ms = time_matmul(size, "cpu")

        if torch.cuda.is_available():
            gpu_ms = time_matmul(size, "cuda")
        else:
            gpu_ms = reference_gpu_ms[size]

        print(f"{size:>6}x{size:<5} | {cpu_ms:>9.1f} | {gpu_ms:>9.1f} | {cpu_ms / gpu_ms:>7.1f}x")

    print()
    print("Small matrices barely gain — sending data to the GPU eats the benefit.")
    print("Large matrices get 10-100x faster: thousands of cores work at once.")


if __name__ == "__main__":
    main()
