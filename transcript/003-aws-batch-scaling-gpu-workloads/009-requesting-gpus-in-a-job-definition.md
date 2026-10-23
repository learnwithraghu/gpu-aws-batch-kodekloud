# Video 009 — Requesting GPUs in a Job Definition

**Section:** 003 — AWS Batch: Scaling GPU Workloads
**Lecture#:** 009
**Sheet title:** Requesting GPUs in a Job Definition
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 003-009-requesting-gpus-in-a-job-defin

---

A job definition can look complete and still never place.

How? By asking the scheduler for a resource profile the target machine cannot actually give.

This is where GPU requests become concrete. In the job definition, you declare that the container needs a GPU, along with CPU and memory. Batch then looks for a compute environment whose instances can satisfy that whole request together.

The trap beginners hit on a sixteen-gigabyte GPU instance is memory math. The host advertises sixteen gibibytes of RAM, but the operating system and container agent keep a slice for themselves. Ask for the full sixteen gibibytes for the task, and the job can sit forever with a resource misconfiguration — ready in theory, placeable nowhere.

That is why KodeFood’s working recipe asks for twelve gibibytes of memory on that instance shape, plus one GPU. The number is not arbitrary. It is the difference between a contract that fits and a contract that blocks.

Make one prediction. If a job stays runnable and never produces application logs, do not start debugging Python first. Ask whether the resource request still fits the machine Batch is allowed to launch.

So the mental model is simple. Declaring a GPU is necessary. Declaring a placeable combination of GPU, CPU, and memory is what actually lets the container start.

Next, we zoom out from the request fields to the instance families themselves — which GPU shapes fit inference jobs like ours, and which belong to large training clusters.

---

## Further reading (not spoken)

- [AWS Batch: GPU jobs](https://docs.aws.amazon.com/batch/latest/userguide/gpu-jobs.html) — requiring GPUs on Batch job definitions
- [AWS Batch: Resource requirements](https://docs.aws.amazon.com/batch/latest/userguide/job_definitions.html#containerproperties.resourceRequirements) — GPU, vCPU, and memory
- [Amazon ECS: Memory management](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/memory-management.html) — why host RAM is not fully task-allocatable
