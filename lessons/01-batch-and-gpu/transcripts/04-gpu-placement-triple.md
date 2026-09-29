# Video 04 — The GPU placement triple
**Type:** Theory
**Runtime target:** ~3 minutes

---

Okay. Here's the thing about GPU placement.

Placement is Batch deciding which EC2 instance, if any, satisfies this job's resource request. For a GPU job, three settings have to agree, or the job never reaches RUNNING. GPUs are scarce, and they are specialized. The scheduler has to line up the host, meaning the driver and the device, the job's request, meaning GPU count and memory, and the compute environment, meaning which instance types are allowed. One wrong field blocks placement. Often you get no application logs, because the container never started.

Treat the three settings as three padlocks on one door. The door is labeled RUNNING.

One lock is the host image type, ECS_AL2023_NVIDIA, or an equivalent. That image has the NVIDIA drivers and the ECS agent, so a container can see CUDA. A plain Amazon Linux AMI on a g4dn can boot a box that looks like a GPU machine, and the container still has no CUDA device. The GPU stays invisible inside.

The next lock is the job definition. The resource requirement is type GPU, value one. Batch places that job only where one GPU is available. It will not place it on a CPU-only shape.

The last lock is memory, and the request has to fit in usable RAM. A g4dn.xlarge advertises sixteen gibibytes. ECS keeps some of that for the operating system and the agent. This course uses twelve thousand two hundred eighty-eight mebibytes. Ask for sixteen thousand three hundred eighty-four mebibytes and the status reason comes back MISCONFIGURATION:JOB_RESOURCE_REQUIREMENT. The job stays RUNNABLE. It never leaves that state. Revision one of gpu-teaching-caption-job is the revision that asks for sixteen thousand three hundred eighty-four. Revision three and later are the ones that place.

Here is the story to recognize. The job has been RUNNABLE for twenty minutes. You open CloudWatch and it is empty. The temptation is to edit the Python. The container never started, so the Python never ran. The fix is to describe the job definitions, lower the memory from sixteen thousand three hundred eighty-four mebibytes to twelve thousand two hundred eighty-eight, and confirm that the GPU requirement is one and that the compute environment's instance types include g4dn.xlarge. Host image, GPU request, and memory are independent. You need all three before RUNNING opens.

This course puts one catalog job on one whole g4dn. Why a T4 at that size is enough, and why we do not slice the machine up, is next.
