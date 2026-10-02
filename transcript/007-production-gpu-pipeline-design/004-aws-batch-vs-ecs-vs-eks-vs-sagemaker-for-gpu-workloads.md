# Video 004 — AWS Batch vs ECS vs EKS vs SageMaker for GPU Workloads

**Section:** 007 — Production GPU Pipeline Design
**Lecture#:** 004
**Sheet title:** AWS Batch vs ECS vs EKS vs SageMaker for GPU Workloads
**Type:** Video
**Runtime target:** ~3 minutes
**Topic code:** 007-004-aws-batch-vs-ecs-vs-eks-vs-

---

Four services usually enter an AWS GPU design review: Batch, ECS, EKS, and SageMaker. They are not interchangeable. Each places a different operating responsibility on the team. We will compare them against the KodeFood workload.

AWS Batch schedules finite work. You define jobs, queues, and compute environments; Batch launches EC2 GPU capacity, places containers, handles retries, and can scale toward zero. KodeFood follows the lifecycle from SUBMITTED to RUNNABLE, RUNNING, and SUCCEEDED, with the CSV stored in S3. Batch may use ECS or EKS underneath, but the operator thinks in jobs rather than always-on services. It fits queued, restartable work.

Amazon ECS orchestrates tasks and services. GPU workloads run on EC2 with GPU-optimized AMIs; Fargate is not the NVIDIA GPU option for this design. ECS fits a long-running caption API, sidecars, or a service mesh that must remain warm. In return, the team owns more of the fleet-health and service-availability work.

Amazon EKS is Kubernetes on AWS. The team manages GPU nodes, drivers, device plugins, and bin-packing within its Kubernetes platform. EKS is a strong choice when Pods, CRDs, and GitOps are already the company standard and batch is one workload among many. Batch on EKS adds Batch queue semantics to Kubernetes capacity. Without it, the team must provide scheduling through tools such as Volcano, Kueue, or custom controllers.

Amazon SageMaker manages the ML lifecycle: training, processing, endpoints, experiments, and model registration. It is appropriate when those capabilities are part of the requirement. For KodeFood, we already have a container and need it to run when a folder appears, so the broader ML platform would add responsibilities without solving a new problem.

The mapping is straightforward. Overnight caption backfills go to Batch. Interactive photo checks need ECS or a SageMaker real-time endpoint with a warm model. A Kubernetes-centered platform points toward EKS, possibly with Batch on EKS. Managed fine-tuning experiments point toward SageMaker Training.

All four still face scarce GPUs, uneven Regional inventory, and the cost of idle devices. The service changes the control plane, not the physical constraint.

That closes the service decision. Next we widen the view and examine why GPU capacity is also a supply-chain, economic, and policy concern.

---

## Further reading (not spoken)

- [AWS Batch User Guide](https://docs.aws.amazon.com/batch/) — batch scheduling on ECS and EKS
- [Amazon ECS: GPU workloads](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-gpu.html) — GPU tasks on EC2
- [Amazon EKS: GPU workloads](https://docs.aws.amazon.com/eks/latest/userguide/gpu-ami.html) — GPU nodes and AMIs on Kubernetes
- [Amazon SageMaker AI Developer Guide](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html) — managed training and inference
- [AWS Batch support for SageMaker Training jobs](https://aws.amazon.com/blogs/machine-learning/introducing-aws-batch-support-for-amazon-sagemaker-training-jobs/) — queueing managed training
