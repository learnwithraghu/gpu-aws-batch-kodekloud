# Video 002 — NVIDIA ECS-Optimized AMIs and GPU Drivers

**Section:** 005 — Building the AWS Batch GPU Infrastructure
**Lecture#:** 002
**Sheet title:** NVIDIA ECS-Optimized AMIs and GPU Drivers
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 005-002-nvidia-ecs-optimized-amis-and-

---

Suppose the machine launches, but the workload still cannot really use the GPU. What went wrong?

Very often, the answer is that the host side and the container side did not meet correctly.

This is one of the easiest things to miss in GPU infrastructure. A GPU workload is not only about the application image. The underlying machine also has to expose the device properly. If that host path is wrong, the container may start, but the workload still behaves as if no usable GPU exists.

That is why the machine image matters so much. Good teams do not want to rebuild GPU driver setup from scratch every time a new machine boots. They want a known-good host foundation that already understands how to run GPU containers reliably.

So the clean mental model is this: part of the GPU path lives on the host, and part of it lives in the container. Both sides have to align.

This is another example of why production GPU work is layered. The application can be correct, the job definition can be correct, and the scheduler can be correct, but if the host GPU path is broken, the workload still fails before any business value is created.

Next, we move from technical compatibility to operational permissions and separate who is allowed to do what in AWS Batch.

---

## Further reading (not spoken)

- [Amazon ECS-optimized Linux AMIs](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html) — including NVIDIA GPU variants
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/index.html) — how containers access the host GPU
- [AWS Batch: GPU jobs](https://docs.aws.amazon.com/batch/latest/userguide/gpu-jobs.html) — requiring GPUs on Batch jobs
