# Video 004 — Understanding GPU Micro-Batching

**Section:** 003 — Building the GPU Application
**Lecture#:** 004
**Sheet title:** Understanding GPU Micro-Batching
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 003-004-understanding-gpu-micro-batchi

---

Inference produces the captions. Micro-batching controls how many photos share one GPU pass.

The T4 on `g4dn.xlarge` has limited device memory. Model weights already use part of it. Each JPEG is also decoded into RGB tensors, which occupy more memory than the compressed object in S3. Sending all thirty vendor photos to BLIP at once can cause an out-of-memory error, even when the folder looks small.

The loop therefore uses `GROUP_SIZE`, set by the `BATCH_SIZE` environment variable. The default is eight. Thirty photos become groups of eight, eight, eight, and six. Each group gets one generate call, and its results join the same list. At the end, `photos.py` writes one CSV.

Notice the naming distinction. AWS Batch groups jobs and queues. Inside our container, `BATCH_SIZE` means photos per GPU forward pass. These are different layers.

Eight is a safe starting point for this model and instance class. A larger model, higher image resolution, or different GPU may need another value. If this breaks with a CUDA out-of-memory message, reduce `BATCH_SIZE` first. If memory is comfortable but the GPU is underused, test a larger value and measure.

Micro-batching changes memory use, not the output contract. One successful job still overwrites `descriptions/<stem>/descriptions.csv`; the groups do not create separate files.

With that loop clear, we can look underneath it. The next lesson connects CUDA, PyTorch, and the container image that makes the T4 usable.

---

## Further reading (not spoken)

- [NVIDIA T4 Tensor Core GPU](https://www.nvidia.com/en-us/data-center/tesla-t4/) — the accelerator on g4dn.xlarge
- [AWS: Amazon EC2 G4 instances](https://aws.amazon.com/ec2/instance-types/g4/) — instance class used for this inference job
- [PyTorch CUDA semantics](https://pytorch.org/docs/stable/notes/cuda.html) — device memory and CUDA behavior in PyTorch
