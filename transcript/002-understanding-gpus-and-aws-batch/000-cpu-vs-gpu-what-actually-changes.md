# Video 000 — CPU vs GPU: What Actually Changes?
**Section:** 002 — Understanding GPUs and AWS Batch
**Lecture#:** 000
**Sheet title:** CPU vs GPU: What Actually Changes?
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 002-000-cpu-vs-gpu--what-actually-chan

---

At the end of section one, we had captions and accept-or-reject decisions. Let’s make the CPU and GPU roles in that path concrete.

A CPU is built for flexible control flow, using a few powerful cores. It is well suited to orchestration: listing objects in S3, downloading files, opening images, writing a CSV, and calling APIs. The `photos.py` side of our job is CPU work even when a GPU is attached.

A GPU is built for throughput on uniform math, using thousands of smaller cores. It is well suited to the BLIP forward pass: receive image tensors, run matrix multiplications, and emit caption tokens. That is the path `describe_items.py` uses when `torch` reports `cuda`.

Moving the caption loop to a GPU changes more than speed. A thirty-photo folder can finish in a short run, but we also gain new failure modes. GPU memory can fill up. Drivers can be incompatible. The container may not see the device. The same Python can run on CPU if that fallback is allowed, but it will be slower.

Treat this as an intentional split. I/O and policy stay on the CPU side. Tensor inference uses the GPU. We ask AWS for a GPU when a folder is waiting, not because every line of Python needs CUDA.

The next constraint is memory. Let’s see how much work the GPU can hold at once, and why we send a few photos at a time instead of the whole folder.

---

## Further reading (not spoken)

- https://developer.nvidia.com/blog/cuda-refresher-reviewing-the-origins-of-gpu-computing/ — clear refresher on why GPUs differ from CPUs
- https://pytorch.org/docs/stable/notes/cuda.html — how PyTorch exposes CUDA devices to application code
