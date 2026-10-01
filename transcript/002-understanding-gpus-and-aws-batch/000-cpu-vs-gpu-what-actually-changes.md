# Video 000 — CPU vs GPU: What Actually Changes?
**Section:** 002 — Understanding GPUs and AWS Batch
**Lecture#:** 000
**Sheet title:** CPU vs GPU: What Actually Changes?
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 002-000-cpu-vs-gpu--what-actually-chan

---

At the end of section one we had captions and accept-or-reject decisions. That decision path only stays fast if the heavy vision math lands on the right kind of chip. So let’s make the CPU versus GPU contrast concrete for KodeFood.

A CPU is optimized for flexible control flow. A few powerful cores. Great at orchestration: list objects in S3, download files, open images, write a CSV, talk to APIs. Our `photos.py` side of the job is essentially CPU work even when a GPU is present.

A GPU is optimized for throughput on uniform math. Thousands of smaller cores. Great at the BLIP forward pass: take image tensors, run matrix multiplies, emit token sequences for captions. That is what `describe_items.py` wants when `torch` reports `cuda`.

What actually changes when you move the caption loop to a GPU? Wall-clock time for a thirty-photo folder drops from “eventually” to “one short run.” You also change the failure modes. Now you care about GPU memory, drivers, and whether the container can see the device. A CPU-only box will still run the same Python — just slowly, and only if you accept that path.

For this course we treat the split as intentional design, not magic. Keep I/O and policy on the CPU side of the process. Keep tensor inference on the GPU. Ask AWS for a GPU instance when a folder is waiting, not because every line of Python needs CUDA.

That's it here for CPU versus GPU at the mental-model level: same math, different shape of machine. The practical question opens next — how much of that GPU memory can you fill at once, and why we caption a handful of photos at a time instead of loading the whole folder in one shot.

---

## Further reading (not spoken)

- https://developer.nvidia.com/blog/cuda-refresher-reviewing-the-origins-of-gpu-computing/ — clear refresher on why GPUs differ from CPUs
- https://pytorch.org/docs/stable/notes/cuda.html — how PyTorch exposes CUDA devices to application code
