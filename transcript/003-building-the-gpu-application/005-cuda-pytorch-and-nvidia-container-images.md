# Video 005 — CUDA, PyTorch and NVIDIA Container Images

**Section:** 003 — Building the GPU Application
**Lecture#:** 005
**Sheet title:** CUDA, PyTorch and NVIDIA Container Images
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 003-005-cuda--pytorch-and-nvidia-conta

---

Micro-batching assumes the model can talk to the GPU. That conversation needs a matched stack.

CUDA is NVIDIA’s platform for running parallel code on the GPU. PyTorch, in our job, is the framework that loads BLIP and calls into CUDA. Transformers sits on top and gives us the BLIP processor and generate API. If those versions disagree, the container can fail at import — before a single photo is captioned.

You could install all of that by hand on every machine. Production teams almost never do. They start from a maintained base image that already pairs a CUDA runtime with a CUDA-enabled PyTorch build. Our Dockerfile starts from `pytorch/pytorch` with CUDA 11.8 and cuDNN in the tag. That choice matches the T4 path we use on Batch.

NVIDIA’s NGC catalog follows the same idea at larger scale: curated containers for frameworks so engineers do not rebuild CUDA toolchains from scratch for every project. Cloud GPU jobs inherit that habit. The host still needs NVIDIA drivers — on Batch, that comes from the NVIDIA ECS-optimized AMI. The container carries the libraries and the app. Drivers on the host, CUDA runtime and framework in the image. Both matter.

Pinning dependencies is part of the same story. This course pins `transformers` to a version that works with the PyTorch 2.1 base. A floating `pip install` next month can pull a release that expects a newer torch and breaks a previously healthy image.

So when we say “GPU application,” we mean more than two Python files. We mean a versioned stack that makes `Device: cuda` possible.

How do we package that stack so every Batch run starts from the same filesystem? That is Docker — and it is the next video.

---

## Further reading (not spoken)

- [NVIDIA CUDA Zone](https://developer.nvidia.com/cuda-zone) — CUDA platform overview
- [PyTorch Docker Hub tags](https://hub.docker.com/r/pytorch/pytorch/tags) — official PyTorch+CUDA images
- [NVIDIA NGC Catalog](https://catalog.ngc.nvidia.com/) — curated GPU containers used widely in industry
