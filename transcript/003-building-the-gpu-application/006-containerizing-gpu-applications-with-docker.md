# Video 006 — Containerizing GPU Applications with Docker

**Section:** 003 — Building the GPU Application
**Lecture#:** 006
**Sheet title:** Containerizing GPU Applications with Docker
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 003-006-containerizing-gpu-application

---

We now have the application and its CUDA-PyTorch stack. Docker packages both as one runnable unit.

Every GPU Batch job needs the same application filesystem: CUDA runtime libraries, PyTorch, transformers, `photos.py`, and `describe_items.py`. The container provides that filesystem on a fresh `g4dn` instance. The image holds the program; S3 holds the data.

Our Dockerfile stays small. It starts from the PyTorch CUDA runtime base, installs the pinned GPU requirements, and copies both scripts into `/app`. The order supports layer caching. If only `describe_items.py` changes, Docker can reuse the expensive dependency layer. If requirements change, that layer must build again. Expect the first build to be slow and code-only rebuilds to be faster.

On an Apple Silicon laptop, include `--platform linux/amd64`. Batch’s `g4dn.xlarge` is x86_64. Without that flag, Docker may produce an arm64 image. The push can succeed, but the Batch worker cannot run it. If the container fails before Python starts with an architecture error, inspect the image platform.

A local tag is also not a deployable image. `gpu-teaching:latest` on your laptop only identifies an image in the local Docker cache. AWS Batch cannot pull from that cache.

The container now gives us a repeatable entrypoint and dependency set. In the next section, we move it to a registry that GPU workers can reach.

---

## Further reading (not spoken)

- [Docker: Multi-platform builds](https://docs.docker.com/build/building/multi-platform/) — why `--platform linux/amd64` matters
- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/) — layers, FROM, COPY, and build caching
- [AWS Batch: Create a job definition](https://docs.aws.amazon.com/batch/latest/userguide/create-job-definition.html) — container image as part of the job template
