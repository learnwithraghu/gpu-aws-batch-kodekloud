# Video 07 — Queue and compute environment binding
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

A job queue is the entrance for submitted work. You do not hand Batch an instance ID. You name a queue. Each queue holds an ordered list of compute environments, with a priority on the queue and an order on each environment. Batch tries to place the job on the first healthy environment in that list. If it cannot, it may try the next environment on that same queue. It will not wander off to some other GPU in the account. A job submitted to gpu-teaching-gpu-smoke-queue-spot runs only on environments attached to that queue.

Queues exist so you can separate kinds of work without teaching every submitter how to boot a machine. One line for cheap interruptible capacity. Another line for capacity you are willing to pay on demand. The submitter chooses the line. Batch chooses the instance inside the pool that line is tied to. In a company, that might be overnight work on Spot and a payroll job on demand. In this course, it is two smoke lanes, and they do not cross.

Lane A is the default. The queue is gpu-teaching-gpu-smoke-queue-spot. State enabled, priority one. Its compute environment order is order one, environment gpu-teaching-gpu-smoke-ce-spot. That environment is Spot, allocation strategy SPOT_CAPACITY_OPTIMIZED, instance type g4dn.xlarge, minimum vCPUs zero, maximum vCPUs four. Spot is cheaper, and it can sit when capacity is tight. A job can stay RUNNABLE because Spot has nothing to give you. That wait is not a broken job definition.

Lane B is the fallback. The queue is gpu-teaching-gpu-smoke-queue-on-demand, also priority one, bound with order one to gpu-teaching-gpu-smoke-ce-on-demand. That environment uses purchase type EC2, the on-demand shape, same instance type and the same vCPU limits. It is steadier when the quota allows it. There is no arrow from the Spot queue to the on-demand environment. Submitting to Spot never silently uses on-demand capacity because Spot is quiet. If you want the other lane, you submit to the other queue, or you change what the queue is bound to. You do not get there by editing the Docker image, and you do not get there by staring at the job definition.

On demand has a quota gate from lesson one. The code is L-DB2E81BA, G and VT instances. Stay on the Spot queue until that quota is at least four vCPUs, one g4dn.xlarge. On demand is the fallback after that quota is approved. When on-demand jobs never start and Spot jobs do, check that quota before you blame Batch.

Create a queue only after its compute environment status is VALID. The binding is in the create call, compute environment order pointing at that environment. Afterward, describe the queue. You want state ENABLED and status VALID, and you want the order list to name the environment you think it names. The env file stores the Spot queue as BATCH_JOB_QUEUE. Lesson eight submits to that name unless you deliberately switch lanes.

On the screen, two conveyor belts leave the submit-job call and never cross. The left belt is tagged with the Spot queue name and ends at the Spot environment. The right belt is tagged with the on-demand queue name and ends at the on-demand environment. A job ID sticker shows the queue, not an instance ID.

Those names already exist in this account. The next clip is the habit that keeps a second pool from appearing beside them.
