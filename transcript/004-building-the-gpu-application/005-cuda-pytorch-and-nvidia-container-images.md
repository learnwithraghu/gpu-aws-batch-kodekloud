# Video 005 — CUDA, PyTorch and NVIDIA Container Images

**Section:** 004 — Building the GPU Application
**Lecture#:** 005
**Sheet title:** CUDA, PyTorch and NVIDIA Container Images
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 004-005-cuda--pytorch-and-nvidia-conta

---

When people first hear "GPU application," they often imagine only model code. But in practice, a GPU workload depends on a whole software stack.

That stack has to line up correctly before the model can do anything useful.

CUDA is the layer that lets software use NVIDIA GPUs. PyTorch is the framework that speaks to that layer for our workload. The model and its supporting libraries sit above that. If those layers do not fit together properly, the job may fail before any image is processed.

This is a very real company concern. Teams do not just manage application logic. They manage compatibility. A model can be correct, and the infrastructure can be available, and the job can still fail because the software stack is mismatched.

That is why versioning matters so much in GPU work. Stability is not only about your own code. It is also about keeping the framework, CUDA support, and container environment aligned well enough that the workload can reliably reach the GPU.

So the key lesson here is broader than one tool or one library. A GPU workload is really a layered system. The model sits at the top, but it depends on everything underneath behaving correctly.

Next, we package that layered system into a container so the same environment can be started again and again on fresh infrastructure.

---

## Further reading (not spoken)

- [NVIDIA CUDA Zone](https://developer.nvidia.com/cuda-zone) — CUDA platform overview
- [PyTorch Docker Hub tags](https://hub.docker.com/r/pytorch/pytorch/tags) — official PyTorch+CUDA images
- [NVIDIA NGC Catalog](https://catalog.ngc.nvidia.com/) — curated GPU containers used widely in industry
