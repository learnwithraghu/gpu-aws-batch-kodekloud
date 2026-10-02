# Video 000 — AWS Batch Compute Environments Explained

**Section:** 005 — Building the AWS Batch GPU Infrastructure
**Lecture#:** 000
**Sheet title:** AWS Batch Compute Environments Explained
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 005-000-aws-batch-compute-environments

---

We already have a clean contract: vendor photos live under one S3 prefix, and captions land under another. The container knows how to follow that contract. What it still needs is a place to run.

That place is a compute environment. In AWS Batch, it defines the pool of machines Batch may grow and shrink for you. KodeFood uses managed compute environments, so Batch creates and removes the EC2 instances. We do not SSH in and start a GPU machine for each vendor folder.

Our teaching setup keeps `minvCpus` at zero. An empty queue means zero desired capacity, so no `g4dn.xlarge` sits idle between jobs. When a caption job arrives, Batch scales up. When it finishes, capacity can return toward zero. That scale-to-zero pattern fits bursty catalog work and keeps the lab bill controlled.

Now look at what belongs on the environment rather than in the Python script: the instance type, typically `g4dn.xlarge` with one NVIDIA T4; Spot or on-demand capacity; maximum vCPUs; subnet and security group; and the AMI that carries the GPU drivers. Together, those settings control cost, reachability, and what Batch is allowed to launch.

For this lab, picture one wave of work. The machines appear for that wave, then disappear. The default is one Spot GPU environment, with an on-demand twin as a fallback when Spot cannot place the job.

Keep that boundary clear: the compute environment defines the pool rules, including the rule that no machine is needed while the queue is quiet. Next, we follow a waiting job as Batch looks for a GPU machine.

---

## Further reading (not spoken)

- [AWS Batch: Compute environments](https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html) — managed vs unmanaged, scaling knobs
- [Amazon EC2 G4 instances](https://aws.amazon.com/ec2/instance-types/g4/) — T4 GPU shape used in this course
