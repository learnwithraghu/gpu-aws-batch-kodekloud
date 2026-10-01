# Video 004 — Understanding GPU Micro-Batching

**Section:** 003 — Building the GPU Application
**Lecture#:** 004
**Sheet title:** Understanding GPU Micro-Batching
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 003-004-understanding-gpu-micro-batchi

---

Inference generates captions. Micro-batching decides how many photos share one GPU pass.

A T4 on `g4dn.xlarge` has limited device memory. The model weights already occupy a large slice. Each photo becomes decoded RGB tensors, not the tiny JPEG size you saw on S3. Hand BLIP all thirty vendor photos in one shot and you risk out-of-memory errors or thrashing — even when the folder looks “small” in megabytes.

So the loop uses `GROUP_SIZE`, driven by the `BATCH_SIZE` environment variable, default eight. Thirty photos become groups of eight, eight, eight, and six. Each group is one generate call. Results append to one list. At the end, `photos.py` writes a single CSV. Micro-batches are a memory tactic, not a product split. You still get one catalog file per vendor folder.

Notice the naming trap. AWS Batch also uses the word “batch” for jobs and queues. Here `BATCH_SIZE` means photos per GPU forward pass inside the container. Eight is chosen to fit this model on this instance class for this course. Change the model, the resolution, or the instance, and you may need a different number.

Teams that serve vision models in production tune the same knob. They measure occupancy and OOM rates, then pick a group size that keeps the GPU busy without spilling memory. Our default is a teaching-safe starting point, not a universal law.

What does not change: one successful job still overwrites `descriptions/<stem>/descriptions.csv`. Groups do not become eight separate outputs.

That's it here for micro-batching: small groups that fit VRAM, repeated until the folder is done. Under that loop sits a stack you should recognize before you build the image — CUDA, PyTorch, and why NVIDIA-friendly container images exist.

---

## Further reading (not spoken)

- [NVIDIA T4 Tensor Core GPU](https://www.nvidia.com/en-us/data-center/tesla-t4/) — the accelerator on g4dn.xlarge
- [AWS: Amazon EC2 G4 instances](https://aws.amazon.com/ec2/instance-types/g4/) — instance class used for this inference job
- [PyTorch CUDA semantics](https://pytorch.org/docs/stable/notes/cuda.html) — device memory and CUDA behavior in PyTorch
