# Video 07 — Spot, on-demand, and the quota trap
**Type:** Theory
**Runtime target:** ~3 minutes

---

Alright. Spot and on demand look similar until a job gets stuck.

Spot and on demand are two ways to get the same shape of machine. A Spot instance is unused EC2 capacity, sold at a discount. AWS can interrupt it, with notice, when that capacity is needed somewhere else. An on demand instance is the normal per-second price, and AWS does not reclaim it the way Spot can. The default environment in this course buys Spot, allocation strategy SPOT_CAPACITY_OPTIMIZED. The names are gpu-teaching-gpu-smoke-ce-spot and gpu-teaching-gpu-smoke-queue-spot. The fallback is the same instance type on demand, gpu-teaching-gpu-smoke-ce-on-demand and gpu-teaching-gpu-smoke-queue-on-demand. On demand is not automatic. A queue does not hop over to it because Spot is quiet.

Service quotas are account limits on how many vCPUs of a family you may run. They are independent of whether a compute environment looks healthy. g4dn is in the G and VT family. L-DB2E81BA is Running On-Demand G and VT instances. It has to be at least four before a g4dn.xlarge on demand job can start. L-3819A6DF is All G and VT Spot Instance Requests. This teaching account uses eight on that Spot quota. Many new accounts default on-demand G and VT to zero. Spot can have room while on demand is still zero.

That zero is the trap. The on demand compute environment and queue can look VALID and Healthy, and every job still stays RUNNABLE forever. No instance. No container. No CloudWatch logs. That is an account limit, not a Batch misconfiguration. A different RUNNABLE, several minutes on the Spot queue, is almost always no Spot capacity right now. Lesson eight switches the queue. Treat the on demand queue as a real fallback only after on-demand G and VT is at least four.

The path people walk is this. Spot feels slow, so they submit to on demand. The job is still RUNNABLE. The check is get-service-quota for L-DB2E81BA. Value zero means request an increase to at least four vCPUs. This course often asks for eight, so one g4dn.xlarge fits with headroom. In the console that is Service Quotas, Amazon EC2, region ap-northeast-1, Running On-Demand G and VT instances. Wait until the case is Approved and get-service-quota shows the new value. The helper helpers/watch_batch_job.sh prints this same quota when a job stays RUNNABLE for about two minutes. Read that line before you touch the image.

Next you run that quota command and read the number it returns.
