# Video 03 — Scale to zero
**Type:** Theory
**Runtime target:** ~3 minutes

---

Alright. Scale to zero is the money move on this compute environment.

Minimum vCPUs set to zero, on a managed compute environment, tells Batch this. When no job needs capacity, desired vCPUs may go to zero. No EC2 instance has to stay running just to keep the environment on the books. Maximum vCPUs is the other end. It caps the burst, so a runaway script cannot request a hundred GPUs.

A GPU instance is priced per second while it is alive. Vendor photo drops can be hours apart. An always-on g4dn is a machine you are paying while the queue is empty. Scale to zero matches the sparse batch inference from the last lesson. You spend during the caption run. When the CSV is written with accepted and rejected rows, and nothing else is waiting, desired capacity can return to zero. This course's compute environments set minimum vCPUs to zero for that reason. When the queue is empty, Batch does not keep a g4dn running.

Walk the clock once. At midnight the queue is empty, desired vCPUs are zero, and spend is flat. At two in the afternoon you call submit-job. Queue depth is one. Batch raises desired vCPUs toward four, which is one g4dn. The instance boots, the container runs, the CSV is written, and the job reaches SUCCEEDED. At about two oh eight the queue is empty again, and capacity drains back to zero. Put an always-on instance on the same chart and the cost is flat, day and night.

You do take a cold start after idle. The machine has to boot, pull the image from ECR, and download the model. That wait is part of lesson eight. It is the price of zero idle GPUs. Keep a GPU circling and the next folder starts fast, and you pay for the circling. Send the machine only when a folder asks, and you wait for it to arrive. This course chooses the wait. From two in the afternoon until about two oh eight, the machine you pay for is that one g4dn, four vCPUs, alive only while the job needs it. Before and after, desired vCPUs are zero. The economics work because the next vendor folder is not already sitting in the queue.

A job can be queued and still never see a GPU. Placement needs the machine image, a GPU request of one, and an honest memory number. That triple is next.
