# Video 006 — Containerizing GPU Applications with Docker

**Section:** 003 — Building the GPU Application
**Lecture#:** 006
**Sheet title:** Containerizing GPU Applications with Docker
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 003-006-containerizing-gpu-application

---

We have the application and the CUDA-PyTorch stack. Docker is how we freeze both into one runnable unit.

A GPU Batch job needs the same filesystem every time it starts: CUDA runtime libraries, PyTorch, transformers, `photos.py`, and `describe_items.py`. A container packages that app-side stack so a fresh `g4dn` does not require you to SSH in and pip-install by hand. The image is the program. S3 remains the data.

Our Dockerfile is deliberately thin. Start from the PyTorch CUDA runtime base. Install the pinned GPU requirements. Copy the two lesson scripts into `/app`. Layer order matters for caching: change only `describe_items.py`, and Docker reuses the heavy pip layer. Change requirements, and pip runs again. First builds feel slow. Code-only rebuilds should feel much faster.

There is one flag you must not forget on Apple Silicon laptops: `--platform linux/amd64`. Batch’s `g4dn.xlarge` is x86_64. Without the platform flag, Docker may build arm64 by default. That image can push cleanly and still fail when the GPU instance tries to run it. The mismatch shows up at job time, not at build time.

Also remember what a local tag is not. `gpu-teaching:latest` on your laptop means your machine has an image. AWS Batch cannot pull from your laptop. Until the image lives in a registry the instance can reach, the job definition is pointing at something else — or at nothing useful.

So why did we containerize? Same entrypoint, same dependencies, every run. The open question now is where that image must live so a worker in your account can pull it. That is the start of the next section: container registries, and why Batch depends on them.

---

## Further reading (not spoken)

- [Docker: Multi-platform builds](https://docs.docker.com/build/building/multi-platform/) — why `--platform linux/amd64` matters
- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/) — layers, FROM, COPY, and build caching
- [AWS Batch: Create a job definition](https://docs.aws.amazon.com/batch/latest/userguide/create-job-definition.html) — container image as part of the job template
