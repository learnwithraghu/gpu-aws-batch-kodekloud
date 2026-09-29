# Video 01 — Why containers for GPU jobs
**Type:** Theory
**Runtime target:** ~3 minutes

---

Hello. Let's start with why this GPU job ships as a container.

A container is a filesystem plus runtime config, packaged with your app, and started as an isolated process on a host. For this GPU job, that package is how you pin the stack the process will see. CUDA user-space libraries, a PyTorch build that can talk to CUDA, the Python packages, and the two scripts from lesson two, all travel together as one artifact a machine can pull. Every Batch run starts from that same filesystem. You don't get a surprise because the cluster pip-installed a different transformers than the one you tested.

Batch uses containers because the alternative is "it worked on my laptop." A GPU job needs a matching stack, and the pieces live in two places. The host, the AMI, provides the NVIDIA drivers and the ECS agent. This course uses the NVIDIA ECS AMI from lessons one and seven for that host side. The image provides the CUDA runtime libraries, PyTorch, transformers, and your scripts. The container isn't a substitute for the driver on the instance. If the AMI is a plain image with no NVIDIA driver, the GPU can be physically present and torch.cuda.is_available still comes back false. describe_items.py then prints cpu, and you're on the wrong machine even though the Python files are correct. If the image is missing the matching CUDA runtime or the pinned packages, the driver on the host can't save you. Missing either side breaks the job.

The Dockerfile in this repo is the app side of that deal. It copies the lesson two files to /app/photos.py and /app/describe_items.py. Batch never sees your repo tree. It never clones Git on the g4dn. It starts python /app/describe_items.py inside whatever image the job definition names. This lesson builds that image on your machine and stops. Lesson four is the push to ECR. Until that push, Batch is still running whatever already sits in the registry.

Count the matching stack as four pieces that have to agree. NVIDIA drivers on the host. CUDA libraries the process can load. A PyTorch build that talks to that CUDA, which is what the base image supplies. Python packages pinned so they still import on that PyTorch. Lesson two prints cuda and calls generate when that agreement holds. Break it and the same script prints cpu, or it exits before a single photo is described.

Next you'll look at the base image this course starts from, and why transformers is pinned.
