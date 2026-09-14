"""
Lesson 02 — job.py
Runs INSIDE the Docker container on the AWS Batch GPU instance.

This script:
  1. Prints which GPU it found
  2. Times a large matrix multiply on that GPU

Nothing else. Goal: prove the GPU is alive and accessible in Batch.
"""
import time
import torch


def main():
    # ── 1. Check GPU ────────────────────────────────────────────────────────
    if not torch.cuda.is_available():
        raise RuntimeError("No GPU found — check the Job Definition's resource requirements.")

    gpu_name   = torch.cuda.get_device_name(0)
    gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9

    print(f"GPU name   : {gpu_name}")
    print(f"GPU memory : {gpu_memory:.1f} GB")

    # ── 2. Matrix multiply on GPU ────────────────────────────────────────────
    SIZE = 5000
    a = torch.randn(SIZE, SIZE, device="cuda")
    b = torch.randn(SIZE, SIZE, device="cuda")

    # Warm-up pass (first call allocates memory, is slower)
    torch.mm(a, b)
    torch.cuda.synchronize()

    # Timed pass
    start = time.perf_counter()
    torch.mm(a, b)
    torch.cuda.synchronize()   # wait for GPU to actually finish
    elapsed_ms = (time.perf_counter() - start) * 1000

    print(f"Matrix size: {SIZE} x {SIZE}")
    print(f"Time       : {elapsed_ms:.1f} ms")
    print("Done.")


if __name__ == "__main__":
    main()
