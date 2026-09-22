"""
Lesson 01 — benchmark_gpu.py
Runs LOCALLY on your machine (no AWS needed).

Times the same matrix multiplication on CPU and (if present) GPU across
three matrix sizes, and prints a simple table.

No local GPU? That's fine — reference times recorded on a g4dn.xlarge
(NVIDIA T4) are used so you still see the comparison. You'll get real GPU
numbers in Lesson 02 when the job runs on AWS Batch.

Usage:
    python benchmark_gpu.py
"""
import time

import torch


def time_matmul(size, device, runs=5):
    """Time a matrix multiply of shape (size x size) on the given device.
    Runs it `runs` times and returns the average milliseconds."""
    a = torch.randn(size, size, device=device)
    b = torch.randn(size, size, device=device)

    # Warm-up: the first run is often slower due to memory allocation
    torch.mm(a, b)
    if device == "cuda":
        torch.cuda.synchronize()   # wait for the GPU to finish before starting the clock

    start = time.perf_counter()
    for _ in range(runs):
        torch.mm(a, b)
        if device == "cuda":
            torch.cuda.synchronize()
    elapsed_ms = (time.perf_counter() - start) / runs * 1000

    return elapsed_ms


def main():
    print(f"PyTorch version : {torch.__version__}")
    print(f"GPU available   : {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        name = torch.cuda.get_device_name(0)
        memory_gb = torch.cuda.get_device_properties(0).total_memory / 1e9
        print(f"GPU name        : {name}")
        print(f"GPU memory      : {memory_gb:.1f} GB")
    print()

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
            print(f"  (no local GPU — using reference T4 time for size {size})")

        print(f"{size:>6}x{size:<5} | {cpu_ms:>9.1f} | {gpu_ms:>9.1f} | {cpu_ms / gpu_ms:>7.1f}x")

    print()
    print("GPUs pay off at scale: small matrices barely gain (data transfer")
    print("overhead), large matrices get 10-100x faster because thousands of")
    print("cores all work at the same time.")


if __name__ == "__main__":
    main()
