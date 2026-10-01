# Video 007 — GPU Quotas and Capacity Constraints
**Section:** 002 — Understanding GPUs and AWS Batch
**Lecture#:** 007
**Sheet title:** GPU Quotas and Capacity Constraints
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 002-007-gpu-quotas-and-capacity-constr

---

Spot versus on-demand only matters if your account is allowed to run the instances. Quotas are where many first GPU jobs get stuck.

EC2 Service Quotas include limits for G and VT instance families — the pool that covers `g4dn` and similar GPU types. Two numbers matter in this course. One limits running on-demand G and VT capacity. Another covers Spot G and VT requests. Brand-new accounts often show on-demand G and VT at zero. Your Batch queue can look valid. Your compute environment can look healthy. Every job still sits in `RUNNABLE` forever: no instance, no container, no CloudWatch logs. That is an account limit, not a broken Dockerfile.

Regional capacity is the second constraint. Even with quota headroom, a busy region may lack Spot GPUs at the moment you submit. The symptom looks similar — long `RUNNABLE` — but the fix differs. Spot scarcity asks for patience or a failover to on-demand. Quota zero asks for a Service Quotas increase and an approved case before on-demand can save you.

For KodeFood teaching we stay on Spot until on-demand G and VT is high enough to fit at least one `g4dn.xlarge` — think at least four vCPUs of quota, with a little headroom if you can get it. Check the quota in Service Quotas before you burn an afternoon debugging Python that never got a machine.

When you request an increase, ask for what the instance needs, wait for approval, and only then treat the on-demand queue as a real fallback.

That’s it here for quotas. Next we pull the whole picture together — a mental map of the AWS Batch GPU architecture we will build on in section three.

---

## Further reading (not spoken)

- https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html — how Service Quotas work
- https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-resource-limits.html — EC2 instance quota concepts, including GPU families
- https://docs.aws.amazon.com/batch/latest/userguide/troubleshooting.html — Batch troubleshooting entry points when jobs never leave RUNNABLE
