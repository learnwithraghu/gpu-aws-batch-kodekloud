# Video 01 — Submit vs run
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

Submit and run are two different moments. Treating them as one moment is how a normal wait gets blamed on the caption program.

aws batch submit-job, or the same action in the console, accepts a job into a queue and returns a job id. That is acceptance. The control plane stored the request. Running means a later set of facts. Batch found capacity, started an instance, pulled the image, and the process inside the container is executing. None of that is implied by the id.

The distinction matters because the id comes back immediately, and it feels like the GPU is captioning. Acceptance is cheap. Capacity is the scarce part, especially Spot g4dn instances in a single availability zone. Batch places the job only when the queue's compute environment can give it the vCPU, the memory, and the GPU the job definition asks for. Until the status reaches STARTING, you read the status, you read statusReason, and you read the compute environment's desired vCPU count. There is no container yet. Changing describe_items.py cannot place a machine.

In this course the queue is gpu-teaching-gpu-smoke-queue-spot, in ap-northeast-1. The job definition name is gpu-teaching-caption-job. You pass that name and Batch uses the highest active revision. You do not pin revision one or revision two. The definition asks for one GPU and twelve thousand two hundred eighty-eight mebibytes of memory. Those numbers are the placement request. Submit only files the request. It does not satisfy it. The fallback queue is gpu-teaching-gpu-smoke-queue-on-demand. It is not a shortcut for a quiet Spot pool. If the on-demand G and VT quota is zero, that queue accepts the job and still never starts a container.

Here is the timeline this course expects, as phases rather than a clock you must hit. At the submit call the status is SUBMITTED. The record exists and validation passed. The job is then often RUNNABLE, sometimes for about thirty seconds and sometimes out toward ten minutes, while Batch searches for Spot capacity or scales the compute environment up from zero. STARTING is the image pull and the container create. RUNNING is when the Python process is executing, which is the first time its log lines can appear. SUCCEEDED means the container exited with code zero.

A package order works the same way. The order placed is the job id. The package on the truck is placement onto a machine. Delivered is the process finishing. The confirmation number is not the delivery.

In this course the slow stretch is usually that RUNNABLE wait, or a cold STARTING on a new instance. It is not BLIP inference on a folder of about thirty photos. Once a GPU is actually running, that folder is a short job. If the status is still RUNNABLE, the model has not been loaded.

On the screen, a timeline bar labels SUBMITTED, RUNNABLE, STARTING, RUNNING, and SUCCEEDED, and the wide empty stretch between the submit call and RUNNING is highlighted. That stretch is capacity, not the model.

Container overrides are next. They are how one template aims at one vendor folder.
