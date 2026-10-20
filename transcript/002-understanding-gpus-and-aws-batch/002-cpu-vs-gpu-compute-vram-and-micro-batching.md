# Video 002 — CPU vs GPU: Compute, VRAM, and Micro-Batching
**Section:** 002 — Understanding GPUs and AWS Batch
**Lecture#:** 002
**Sheet title:** CPU vs GPU: Compute, VRAM, and Micro-Batching
**Type:** Video
**Runtime target:** ~3 minutes
**Topic code:** 002-002-cpu-vs-gpu--compute--vram--and

---

Even on a GPU instance, the GPU does not run the whole program. Production AI workloads split the work between the CPU and the GPU, and manage two separate pools of memory.

The CPU handles control flow and I/O: listing objects in S3, downloading files, opening images, applying the accept-or-reject rule, and writing `descriptions.csv`. In our container, the `photos.py` side is CPU work even when a GPU is attached.

The GPU handles throughput on uniform math. It holds the BLIP model and runs the forward pass that turns image tensors into caption tokens. That is the path `describe_items.py` uses when PyTorch reports `cuda`.

Moving that loop onto a GPU brings speed, but it also introduces a hard boundary: GPU memory, or VRAM. VRAM is physically separate from the instance’s host RAM. Loading BLIP onto an NVIDIA T4 consumes part of that VRAM before the first photo arrives, and every image in a forward pass adds intermediate activations.

If we send all thirty vendor photos into the model in one call, VRAM can fill up and crash the container with an out-of-memory error. Instead, our application uses micro-batching. With a default `BATCH_SIZE` of eight, thirty photos are processed in groups of eight, eight, eight, and six. Each group runs one GPU pass, appends its captions to a single list, and still produces one final CSV.

Larger micro-batches can improve GPU utilization, right up until VRAM becomes the bottleneck. On KodeFood’s `g4dn.xlarge`, eight is a safe operating default that we can tune via an environment variable without changing code.

Keep this mental model sharp: host RAM serves CPU downloads and CSV assembly, while VRAM holds the model and active micro-batch. Adding system memory will never fix a GPU out-of-memory error.

Now that we know how the container uses CPU, GPU, and VRAM, let’s look at where to run it in AWS—and why AWS Batch fits this job.

---

## Further reading (not spoken)

- https://developer.nvidia.com/blog/cuda-refresher-reviewing-the-origins-of-gpu-computing/ — how CPU and GPU execution responsibilities differ
- https://pytorch.org/docs/stable/notes/cuda.html#memory-management — PyTorch CUDA device and VRAM management
