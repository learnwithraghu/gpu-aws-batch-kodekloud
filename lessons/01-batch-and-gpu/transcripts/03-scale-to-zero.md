# Video 03 — Scale to zero
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

Minimum vCPUs set to zero, on a managed compute environment, tells Batch this. When no job needs capacity, desired vCPUs may go to zero. No EC2 instance has to stay running just to keep the environment on the books. Maximum vCPUs is the other end. It caps the burst, so a runaway script cannot request a hundred GPUs.

A GPU instance is priced per second while it is alive. Vendor photo drops, the way menu updates arrive for a regional restaurant chain, can be hours apart. An always-on g4dn is a standby chef you are paying while the dining room is empty. Scale to zero matches the sparse batch inference from the last lesson. You spend during the caption run. When the CSV is written and nothing else is waiting, desired capacity can return to zero. This course's compute environments set minimum vCPUs to zero for that reason. When the queue is empty, Batch does not keep a g4dn running.

Walk the clock once. At midnight the queue is empty, desired vCPUs are zero, and spend is flat. At two in the afternoon you call submit-job. Queue depth is one. Batch raises desired vCPUs toward four, which is one g4dn. The instance boots, the container runs, the CSV is written, and the job reaches SUCCEEDED. At about two oh eight the queue is empty again, and capacity drains back to zero. Put an always-on instance on the same chart and the cost is flat, day and night.

You do take a cold start after idle. The machine has to boot, pull the image from ECR, and download the model. That wait is part of lesson eight. It is the price of zero idle GPUs. It is the same kind of trade Uber makes between how many drivers are already out and how long a rider waits. Keep a driver circling the block and the pickup is fast, and you pay for the circling. Send the driver only when a rider asks, and the rider waits for the car to arrive. This course chooses the wait. From two in the afternoon until about two oh eight, the machine you pay for is that one g4dn, four vCPUs, alive only while the job needs it. Before the empty midnight queue, and after the job reaches SUCCEEDED, desired vCPUs are zero, so there is no instance on the bill. An always-on line through that same stretch would have been paying since midnight for a machine with an empty queue. The cold start is the gap between submit-job and the container actually running. Boot, then the pull from ECR, then the model download. The economics work because the next vendor folder is not already sitting in the queue.

On the screen, queue depth and the EC2 count share one chart. A dollar meter rises only when the depth is above zero.

A job can be queued and still never see a GPU. Placement needs the machine image, a GPU request of one, and an honest memory number. That triple is next.
