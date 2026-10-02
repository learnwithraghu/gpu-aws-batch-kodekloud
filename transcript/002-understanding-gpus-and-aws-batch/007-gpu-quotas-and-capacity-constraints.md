# Video 007 — GPU Quotas and Capacity Constraints
**Section:** 002 — Understanding GPUs and AWS Batch
**Lecture#:** 007
**Sheet title:** GPU Quotas and Capacity Constraints
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 002-007-gpu-quotas-and-capacity-constr

---

Spot versus on-demand matters only after the account is allowed to run the instance. This is where many first GPU jobs get stuck.

EC2 Service Quotas include limits for the G and VT instance families, which cover `g4dn` and similar GPU types. Two quotas matter here: one for running on-demand G and VT capacity, and another for Spot G and VT requests. New accounts often have an on-demand G and VT quota of zero.

In that state, the Batch queue can be valid and the compute environment can be healthy, while every job remains in `RUNNABLE`. No instance starts. No container runs. No CloudWatch application logs appear. That is an account-capacity limit, not evidence of a broken Dockerfile.

Regional availability is a separate constraint. Even with enough quota, a region may not have Spot GPUs available when we submit. The symptom can look similar, but the response is different. Spot scarcity may call for patience or an on-demand fallback. A zero quota requires an approved Service Quotas increase before on-demand can help.

For this KodeFood environment, we stay on Spot until the on-demand G and VT quota can fit at least one `g4dn.xlarge`: at least four vCPUs, with some headroom if available. Check that quota before debugging application code that has not reached a machine.

If a job has no logs and stays `RUNNABLE`, first ask whether it was ever placed. That one check keeps quota and capacity issues separate from container failures.

Next, we’ll assemble the complete AWS Batch GPU path before moving into the application.

---

## Further reading (not spoken)

- https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html — how Service Quotas work
- https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-resource-limits.html — EC2 instance quota concepts, including GPU families
- https://docs.aws.amazon.com/batch/latest/userguide/troubleshooting.html — Batch troubleshooting entry points when jobs never leave RUNNABLE
