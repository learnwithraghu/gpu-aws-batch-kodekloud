# Video 011 — GPU-Ready AMIs and Containers

**Section:** 003 — AWS Batch: Scaling GPU Workloads
**Lecture#:** 011
**Sheet title:** GPU-Ready AMIs and Containers
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 003-011-gpu-ready-amis-and-containers

---

Suppose Batch launches the right GPU instance, and the job still behaves as if no accelerator exists.

What broke?

Very often, the host side and the container side never met correctly.

A GPU workload is two layers. On the host, the machine image needs NVIDIA drivers and the container runtime hooks that expose the device. On the container side, your image needs the CUDA userspace and framework build that can talk to that device. If either layer is wrong, the physical card can be attached to the server while PyTorch still sees zero usable GPUs.

That is why teams prefer known-good ECS-optimized NVIDIA AMIs for Batch GPU environments instead of reinventing driver setup on every boot. The AMI carries the host foundation. Your application image carries the model stack.

The clean mental model is a handshake. Host drivers and runtime open the door. The container walks through with CUDA and the framework. Both sides have to agree.

In a company incident, this distinction saves time. A placement success followed by “no GPU visible” is usually not a queue bug. It is a host-and-container compatibility problem.

So before the GPU Spot demo later in this section, remember: choosing an instance type is not enough. The AMI and the container image are part of the same GPU path.

Next, we ask what changes when one machine is no longer enough — multi-node parallel jobs for training.

---

## Further reading (not spoken)

- [Amazon ECS-optimized Linux AMIs](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html) — including NVIDIA GPU variants
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/index.html) — how containers access the host GPU
- [AWS Batch: GPU jobs](https://docs.aws.amazon.com/batch/latest/userguide/gpu-jobs.html) — GPU-enabled Batch on ECS-optimized AMIs
