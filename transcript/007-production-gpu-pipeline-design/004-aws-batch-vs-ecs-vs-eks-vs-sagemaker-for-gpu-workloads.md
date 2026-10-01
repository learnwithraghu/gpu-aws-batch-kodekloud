# Video 004 — AWS Batch vs ECS vs EKS vs SageMaker for GPU Workloads

**Section:** 007 — Production GPU Pipeline Design
**Lecture#:** 004
**Sheet title:** AWS Batch vs ECS vs EKS vs SageMaker for GPU Workloads
**Type:** Video
**Runtime target:** ~3 minutes
**Topic code:** 007-004-aws-batch-vs-ecs-vs-eks-vs-

---

Four names show up in every “how should we run GPUs on AWS?” meeting. They are not four flavors of the same thing. They solve different operating problems. Let’s put them next to KodeFood so the choice is concrete.

AWS Batch is a scheduler for batch work. You define jobs, queues, and compute environments. Batch decides when to launch EC2 GPU capacity, places containers, retries, and can scale toward zero. You already lived this: submit, RUNNABLE, RUNNING, SUCCEEDED, CSV on S3. Batch can orchestrate on ECS or EKS underneath — but you think in jobs, not in always-on services. Best when work is queued, finite, and restartable.

Amazon ECS is container orchestration. You run tasks and services on EC2 or Fargate. For GPUs you use EC2 with GPU-optimized AMIs — Fargate still does not give you NVIDIA GPUs the way Batch GPU jobs need. ECS shines for long-running caption APIs, sidecars, and service meshes where something must stay warm. You own more of the “keep the fleet healthy” story than Batch does for pure batch.

Amazon EKS is Kubernetes on AWS. Same GPU node problems — drivers, device plugins, bin-packing — plus the Kubernetes control plane your platform team already operates. Choose EKS when the company standardized on Pods, CRDs, and GitOps, and batch is one workload among many. Batch on EKS exists for teams who want Batch’s queue semantics on Kubernetes capacity. Pure EKS without Batch means you build or adopt a queue yourself — Volcano, Kueue, or custom controllers.

Amazon SageMaker is the managed ML platform — training, processing, endpoints, experiments, model registry. Use it when the product is the ML lifecycle, not when you already have a Docker image and only need “run this container on a GPU when a folder appears.” Overkill for KodeFood’s CSV job; underkill if you pretend a training studio is a general batch scheduler.

KodeFood choices: overnight caption backfill → Batch. Interactive “check this photo now” → ECS or SageMaker real-time with a warm model. Platform already on Kubernetes → EKS, maybe Batch-on-EKS. Fine-tuning with managed experiments → SageMaker Training.

All four still share scarce GPUs, uneven Regions, and a bill for idle silicon. The scheduler changes; the constraint does not.

That’s the fork for this infrastructure chapter. Zoom out next — why the world fights over the same accelerators, and why your Batch design matters more when capacity is geopolitical and economic, not just a console checkbox.

---

## Further reading (not spoken)

- [AWS Batch User Guide](https://docs.aws.amazon.com/batch/) — batch scheduling on ECS and EKS
- [Amazon ECS: GPU workloads](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-gpu.html) — GPU tasks on EC2
- [Amazon EKS: GPU workloads](https://docs.aws.amazon.com/eks/latest/userguide/gpu-ami.html) — GPU nodes and AMIs on Kubernetes
- [Amazon SageMaker AI Developer Guide](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html) — managed training and inference
- [AWS Batch support for SageMaker Training jobs](https://aws.amazon.com/blogs/machine-learning/introducing-aws-batch-support-for-amazon-sagemaker-training-jobs/) — queueing managed training
