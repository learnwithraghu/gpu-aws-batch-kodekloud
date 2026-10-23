# Video 010 — GPU Instance Types for Batch

**Section:** 003 — AWS Batch: Scaling GPU Workloads
**Lecture#:** 010
**Sheet title:** GPU Instance Types for Batch
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 003-010-gpu-instance-types-for-batch

---

Not every GPU instance is the right kitchen for KodeFood.

Why does instance family choice matter so much for Batch?

Because the compute environment only offers what you allow, and the job definition only places on machines that fit. Pick the wrong family, and you either overpay for silicon you never saturate, or you wait forever for capacity that your account cannot launch.

In AWS, accelerated instances cluster into familiar groups. G-series shapes — such as the g4dn family with NVIDIA T4 GPUs — are the workhorses for single-GPU inference and light fine-tuning. Newer G generations raise performance for the same class of work. P-series shapes pack multiple high-end GPUs with fast interconnects for large training jobs, at a much higher hourly cost.

KodeFood captioning is inference on one folder at a time. It wants a modest single-GPU machine, not a training supercluster. DoorDash-style catalog pipelines follow the same economic instinct: enough accelerator for the burst, then scale away.

There is a second guardrail beginners miss: account quotas. Even a perfect instance type fails if the account is not allowed to run that many GPU vCPUs on demand or Spot. The job looks valid. The kitchen simply never opens.

So match three things together: workload shape, instance family, and quota reality. Next we look at the host and container layers that must meet before any of those GPUs become visible inside PyTorch.

---

## Further reading (not spoken)

- [Amazon EC2 Accelerated Computing instances](https://aws.amazon.com/ec2/instance-types/#Accelerated_Computing) — G-series and P-series overview
- [Amazon EC2 G4 instances](https://aws.amazon.com/ec2/instance-types/g4/) — T4 GPU shape used for course inference
- [Amazon EC2 service quotas](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-on-demand-instances-limits.html) — G and VT vCPU limits that block placement
