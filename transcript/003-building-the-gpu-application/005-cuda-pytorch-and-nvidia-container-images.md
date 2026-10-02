# Video 005 — CUDA, PyTorch and NVIDIA Container Images

**Section:** 003 — Building the GPU Application
**Lecture#:** 005
**Sheet title:** CUDA, PyTorch and NVIDIA Container Images
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 003-005-cuda--pytorch-and-nvidia-conta

---

Micro-batching only helps after the model can use the GPU. That requires a compatible software stack.

CUDA is NVIDIA’s platform for running parallel work on the GPU. PyTorch loads BLIP and calls CUDA. Transformers provides the BLIP processor and generation API. If these versions are incompatible, the container may fail during import, before it reads a photo.

Our Dockerfile starts from `pytorch/pytorch` with CUDA 11.8 and cuDNN in the tag. That base already pairs a CUDA runtime with a CUDA-enabled PyTorch build for the T4 path used by this Batch job. We do not assemble that toolchain on each temporary instance.

There is also a host side to the stack. The NVIDIA ECS-optimized AMI supplies the GPU driver. The container supplies the CUDA runtime, framework, dependencies, and application. If `Device: cuda` is missing, trace both sides: first GPU and driver availability on the host, then CUDA and PyTorch compatibility in the image.

Dependency pins protect that compatibility. This course pins `transformers` to a version that works with the PyTorch 2.1 base. An unpinned install can later select a release that expects a newer PyTorch version and break an image that previously built.

So our GPU application is not just two Python files. It is a versioned stack that makes `Device: cuda` possible.

Now we need to package that stack into the same filesystem for every run. The Docker lesson shows exactly what goes into the image.

---

## Further reading (not spoken)

- [NVIDIA CUDA Zone](https://developer.nvidia.com/cuda-zone) — CUDA platform overview
- [PyTorch Docker Hub tags](https://hub.docker.com/r/pytorch/pytorch/tags) — official PyTorch+CUDA images
- [NVIDIA NGC Catalog](https://catalog.ngc.nvidia.com/) — curated GPU containers used widely in industry
