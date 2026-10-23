# Video 003 — Compute Environments: EC2, Fargate, and EKS

**Section:** 003 — AWS Batch: Scaling GPU Workloads
**Lecture#:** 003
**Sheet title:** Compute Environments: EC2, Fargate, and EKS
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 003-003-compute-environments-ec2-farga

---

If the compute environment is the kitchen, the next question is: what kind of kitchen can Batch actually open?

AWS Batch can back that kitchen with different orchestrators. EC2-backed environments launch real instances you shape with instance types, purchase options, and often a launch template. Fargate removes instance management for many CPU workloads. EKS-backed environments let Batch place jobs onto a Kubernetes cluster your team already operates.

For KodeFood GPU captioning, the important constraint is simple. GPU Batch jobs need an EC2-backed path — or an EKS path with GPU nodes. Fargate may simplify ordinary containers, but it is not the accelerator path this course uses.

That is why launch templates show up in GPU setups. Teams encode host-level choices once — networking, AMI family, instance profile — so every machine Batch launches starts from a known-good foundation instead of a blank EC2 form.

In a company, this choice is really an ownership decision. Do you want Batch to manage EC2 capacity for finite jobs? Do you already run Kubernetes and want Batch as the job front door? Or are you tempted by Fargate simplicity for a workload that actually needs a GPU?

Make one prediction before the demos. If a design says “GPU job on Fargate,” the platform will push back. The scheduler can be perfect, and the application can be correct, but the wrong compute environment type still blocks the work.

Next, one console demo builds that kitchen end to end: launch template, compute environment, and queue. After that, we open the recipe itself — the anatomy of a job definition.

---

## Further reading (not spoken)

- [AWS Batch: Compute environments](https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html) — managed EC2, Fargate, and EKS options
- [AWS Batch: When to use Fargate](https://docs.aws.amazon.com/batch/latest/userguide/bestpractice4.html) — EC2 required for GPU jobs
- [AWS Batch: Launch templates](https://docs.aws.amazon.com/batch/latest/userguide/launch-templates.html) — encoding AMI, network, and host settings
