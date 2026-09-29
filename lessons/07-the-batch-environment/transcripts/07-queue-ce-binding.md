# Video 07 — Queue and compute environment binding
**Type:** Theory
**Runtime target:** ~3 minutes

---

Here's the thing. A job queue is the entrance for submitted work. You do not hand Batch an instance ID. You name a queue. Each queue holds an ordered list of compute environments. Batch tries the first healthy environment on that list. It will not wander to some other GPU in the account. A job on gpu-teaching-gpu-smoke-queue-spot runs only on environments attached to that queue.

Queues separate kinds of work. One line for cheap interruptible capacity. Another for capacity you pay on demand. The submitter chooses the line. Batch chooses the instance inside that pool. In this course the two smoke lanes do not cross.

Lane A is the default. Queue gpu-teaching-gpu-smoke-queue-spot, enabled, priority one, order one bound to gpu-teaching-gpu-smoke-ce-spot. That environment is Spot, SPOT_CAPACITY_OPTIMIZED, g4dn.xlarge, min vCPUs zero, max four. Spot is cheaper and can sit when capacity is tight. A job can stay RUNNABLE because Spot has nothing to give. That wait is not a broken job definition, and it is not a bug in KodeFood's caption code.

Lane B is the fallback. Queue gpu-teaching-gpu-smoke-queue-on-demand, priority one, bound to gpu-teaching-gpu-smoke-ce-on-demand. Purchase type EC2, same instance type and vCPU limits. There is no arrow from the Spot queue to the on-demand environment. Submitting to Spot never silently uses on-demand because Spot is quiet. If you want the other lane, submit to the other queue. You do not get there by editing the Docker image or staring at the job definition.

On demand has a quota gate. Code L-DB2E81BA, G and VT instances. Stay on Spot until that quota is at least four vCPUs, one g4dn.xlarge. When on-demand jobs never start and Spot jobs do, check that quota before you blame Batch.

Create a queue only after its compute environment is VALID. Bind it in the create call. Afterward describe the queue. You want ENABLED, VALID, and the order list naming the environment you expect. .env stores the Spot queue as BATCH_JOB_QUEUE. Lesson eight submits to that name unless you switch lanes on purpose.

Those names already exist. Next is the habit that keeps a second pool from appearing beside them.
