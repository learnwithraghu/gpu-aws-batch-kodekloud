# Video 01 — Submit vs run
**Type:** Theory
**Runtime target:** ~3 minutes

---

Alright. Welcome back. Submit and run are two different moments. Treating them as one is how a normal wait gets blamed on the caption program.

aws batch submit-job accepts a job into a queue and returns a job id. That is acceptance. The control plane stored the request. Running means Batch found capacity, started an instance, pulled the image, and the process inside is executing. None of that is implied by the id.

The id comes back immediately, so it feels like the GPU is captioning. Acceptance is cheap. Capacity is scarce, especially Spot g4dn in one availability zone. Batch places the job only when the queue's compute environment can give the vCPU, memory, and GPU the definition asks for. Until STARTING, you read status, statusReason, and the compute environment's desired vCPUs. There is no container yet. Changing describe_items.py cannot place a machine.

You submit to the queue and job definition you wired in lesson 07. Their names live in your env file as BATCH_JOB_QUEUE and BATCH_JOB_DEFINITION. Pass the definition by name so Batch uses the highest active revision. The GPU and memory numbers on that revision are the placement request. Submit files it. It does not satisfy it. Switching to an on-demand queue is not a shortcut for quiet Spot. Quotas decide whether that queue can ever start a container. That story is later in this lesson.

Timeline: SUBMITTED when the record exists. Then often RUNNABLE while Batch searches for Spot or scales from zero. STARTING is image pull and container create. RUNNING is when Python executes, the first time its log lines can appear. SUCCEEDED means exit code zero.

The slow stretch is usually that RUNNABLE wait, or a cold STARTING on a new instance. It is not BLIP on a KodeFood vendor folder of about thirty photos. Once a GPU is running, that folder is a short job. If status is still RUNNABLE, the model has not loaded.

Container overrides are next. They aim one template at one vendor folder.
