# Video 001 — GPU Memory, Compute and Micro-Batching
**Section:** 002 — Understanding GPUs and AWS Batch
**Lecture#:** 001
**Sheet title:** GPU Memory, Compute and Micro-Batching
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 002-001-gpu-memory--compute-and-micro-

---

We’ve separated CPU orchestration from GPU math. The next question is not only whether a GPU exists, but how much work it can hold at once.

GPU memory, or VRAM, is finite and separate from the instance’s system RAM. Loading BLIP onto a T4 consumes part of it. Each photo in a forward pass adds activations. If we send all thirty vendor photos in one call, the GPU can run out of memory or spend its time struggling with an oversized working set.

Our application uses micro-batching. The default `BATCH_SIZE` is eight, so thirty photos become groups of eight, eight, eight, and six. Each group takes one GPU pass. Its captions are appended to one list, and the job still produces one CSV. The micro-batches are a memory strategy, not separate product outputs.

A larger batch can improve GPU utilization because each kernel launch carries more work. That only helps until VRAM becomes the limit. For BLIP on KodeFood’s `g4dn.xlarge`, eight is a practical fit. We can tune the environment variable later, but we cannot treat memory as unlimited.

Keep system RAM separate in your mental model. The CPU side still downloads images and builds the CSV. GPU memory holds the model and active micro-batch. If this distinction is wrong, you can easily add host memory while the real limit remains VRAM.

Now that we know the resource shape, let’s decide where the job should run: Lambda, ECS, SageMaker, raw EC2, or Batch.

---

## Further reading (not spoken)

- https://pytorch.org/docs/stable/notes/cuda.html#memory-management — PyTorch notes on CUDA memory behavior
- https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#features-and-technical-specifications — how GPU device memory constrains concurrent work
