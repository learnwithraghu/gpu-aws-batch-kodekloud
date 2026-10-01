# Video 000 — AWS Batch Compute Environments Explained

**Section:** 005 — Building the AWS Batch GPU Infrastructure
**Lecture#:** 000
**Sheet title:** AWS Batch Compute Environments Explained
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 005-000-aws-batch-compute-environments

---

You closed the last section with a clean contract: vendor photos live under an S3 prefix, captions land under another. The container knows how to walk that contract. What it does not have yet is a place to run.

That place is a compute environment. In AWS Batch, a compute environment is the pool of machines Batch is allowed to grow and shrink for you. For KodeFood we use managed compute environments. Managed means Batch creates and tears down the EC2 instances. You do not SSH in to start a GPU box before every vendor folder.

Our teaching setup keeps `minvCpus` at zero. When the queue is empty, desired capacity is zero — no idle `g4dn.xlarge` between jobs. When a caption job lands, Batch scales up. When the job finishes, capacity can fall back toward zero. That scale-to-zero pattern fits bursty catalog work better than an always-on GPU fleet.

Notice what you declare on the environment, not on the Python script. Instance type — typically `g4dn.xlarge` with one NVIDIA T4. Spot versus on-demand. Maximum vCPUs so one account cannot launch an unbounded GPU fleet. Subnet and security group so the instance can reach ECR, S3, and logs. The AMI that already carries GPU drivers.

Think of capacity the way bursty marketplace pipelines do: work arrives in waves, machines appear for the wave, then disappear. Our course version is one Spot GPU environment as the default, with an on-demand twin as a fallback when Spot cannot place.

That's it here for compute environments: the pool rules Batch uses when it needs machines — including none when the queue is quiet. Next we watch how Batch finds a GPU machine and launches it when your job is waiting.

---

## Further reading (not spoken)

- [AWS Batch: Compute environments](https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html) — managed vs unmanaged, scaling knobs
- [Amazon EC2 G4 instances](https://aws.amazon.com/ec2/instance-types/g4/) — T4 GPU shape used in this course
