# Video 004 — Understanding GPU Micro-Batching

**Section:** 004 — Building the GPU Application
**Lecture#:** 004
**Sheet title:** Understanding GPU Micro-Batching
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 004-004-understanding-gpu-micro-batchi

---

Once inference is working, the next practical question is: should the GPU process images one by one, or should it process a few together?

That is where micro-batching comes in.

The idea is simple. A single image may not use the GPU efficiently. But throwing too many images at the GPU at once can exhaust memory. So teams look for a middle ground: a small group size that keeps the device productive without pushing it into failure.

This is a classic production tradeoff. Too small, and you waste expensive GPU time. Too large, and the job becomes unstable or slow for a different reason. The right value is rarely philosophical. It is something you test and tune.

That is also why micro-batching matters so much in real systems. It connects model behavior to infrastructure limits. You are no longer asking only, "does the model work?" You are asking, "does the model work efficiently on this specific hardware profile?"

For this course, the mental model is enough: one job still owns one vendor folder and one final output. Micro-batching changes how the work is processed inside the job. It does not change the external contract of the pipeline.

So think of micro-batching as the bridge between AI logic and GPU operations.

Next, we step down one layer and look at the software stack that makes the GPU usable in the first place.

---

## Further reading (not spoken)

- [NVIDIA T4 Tensor Core GPU](https://www.nvidia.com/en-us/data-center/tesla-t4/) — the accelerator on g4dn.xlarge
- [AWS: Amazon EC2 G4 instances](https://aws.amazon.com/ec2/instance-types/g4/) — instance class used for this inference job
- [PyTorch CUDA semantics](https://pytorch.org/docs/stable/notes/cuda.html) — device memory and CUDA behavior in PyTorch
