# Course transcript index

Course: **Building Production GPU Workloads on AWS**

Source of truth: [`Building Production GPU Workloads on AWS - Draft-Raghu.csv`](../Building%20Production%20GPU%20Workloads%20on%20AWS%20-%20Draft-Raghu.csv). Video scripts are the default. Demo/Lab runbooks are included where drafted (Section 001 manual verification demo/lab; Section 002 Sequential CPU vs Parallel GPU simulator demo/lab; Section 008 final pipeline walkthrough). Two Section 001 stubs still need full scripts (`000` course approach, `006` whiteboard). Section 003 has **3 console demos** (no demo transcripts): [`lessons/03-aws-batch-console/`](../lessons/03-aws-batch-console/README.md).

**Voice:** conversational teleprompter scripts for slide generation. Target **~2 minutes** (about 260–300 words) unless a topic needs **~3 minutes** (up to ~450 words).

**Structure:** `transcript/<section-folder>/<lecture#>-<slug>.md`

| Section | Folder | Videos (sheet) |
|---------|--------|----------------|
| 001 | [001-the-real-world-gpu-problem](001-the-real-world-gpu-problem/) | 4 (+ whiteboard; Demo/Lab separate) |
| 002 | [002-gpu-fundamentals-from-silicon-to-cloud](002-gpu-fundamentals-from-silicon-to-cloud/) | 6 (+ Demo/Lab) |
| 003 | [003-aws-batch-scaling-gpu-workloads](003-aws-batch-scaling-gpu-workloads/) | 13 videos (+ 3 [console demos](../lessons/03-aws-batch-console/)) |
| 004 | [004-building-the-gpu-application](004-building-the-gpu-application/) | 6 |
| 005 | [005-building-the-data-and-container-pipeline](005-building-the-data-and-container-pipeline/) | 4 |
| 006 | [006-building-the-aws-batch-gpu-infrastructure](006-building-the-aws-batch-gpu-infrastructure/) | 7 |
| 007 | [007-running-the-end-to-end-gpu-pipeline](007-running-the-end-to-end-gpu-pipeline/) | 5 |
| 008 | [008-production-gpu-pipeline-design](008-production-gpu-pipeline-design/) | 5 |
| 009 | [009-the-global-gpu-landscape-demand-constraints-regulations](009-the-global-gpu-landscape-demand-constraints-regulations/) | 12 |

## Play order

### 001 — The Real-World GPU Problem

| # | File | Title | Runtime |
|---|------|-------|---------|
| 000 | [000-the-course-approach.md](001-the-real-world-gpu-problem/000-the-course-approach.md) | The course approach | stub |
| 001 | [001-the-kodefood-platform.md](001-the-real-world-gpu-problem/001-the-kodefood-platform.md) | The KodeFood Platform | ~2 min |
| 002 | [002-the-kodefood-problem-processing-vendor-images-at-scale.md](001-the-real-world-gpu-problem/002-the-kodefood-problem-processing-vendor-images-at-scale.md) | The KodeFood Problem: Processing Vendor Images at Scale | ~2 min |
| 006 | [006-whiteboard-visualize-the-high-level-blocks.md](001-the-real-world-gpu-problem/006-whiteboard-visualize-the-high-level-blocks.md) | [Whiteboard] Visualize the high level blocks | stub |
| 007 | [007-demo-current-manual-menu-image-verification.md](001-the-real-world-gpu-problem/007-demo-current-manual-menu-image-verification.md) | [Demo] Current manual menu image verification | ~8–10 min |
| 008 | [008-lab-current-manual-menu-image-verification.md](001-the-real-world-gpu-problem/008-lab-current-manual-menu-image-verification.md) | [Lab] Current manual menu image verification | ~20–30 min |

### 002 — GPU Fundamentals: From Silicon to Cloud

| # | File | Title | Runtime |
|---|------|-------|---------|
| 000 | [000-what-is-a-gpu-really.md](002-gpu-fundamentals-from-silicon-to-cloud/000-what-is-a-gpu-really.md) | What Is a GPU, Really? | ~2 min |
| 001 | [001-from-pixels-to-processors-a-gpu-history.md](002-gpu-fundamentals-from-silicon-to-cloud/001-from-pixels-to-processors-a-gpu-history.md) | From Pixels to Processors: A GPU History | ~2 min |
| 002 | [002-how-gpus-took-over-computing.md](002-gpu-fundamentals-from-silicon-to-cloud/002-how-gpus-took-over-computing.md) | How GPUs Took Over Computing | ~2 min |
| 003 | [003-cpu-vs-gpu-why-we-need-both.md](002-gpu-fundamentals-from-silicon-to-cloud/003-cpu-vs-gpu-why-we-need-both.md) | CPU vs GPU: Why We Need Both | ~2 min |
| 004 | [004-inside-the-gpu-hardware-explained.md](002-gpu-fundamentals-from-silicon-to-cloud/004-inside-the-gpu-hardware-explained.md) | Inside the GPU: Hardware Explained | ~3 min |
| 005 | [005-gpus-in-the-cloud.md](002-gpu-fundamentals-from-silicon-to-cloud/005-gpus-in-the-cloud.md) | GPUs in the Cloud | ~3 min |
| 007 | [007-demo-sequential-cpu-vs-parallel-gpu.md](002-gpu-fundamentals-from-silicon-to-cloud/007-demo-sequential-cpu-vs-parallel-gpu.md) | [Demo] Sequential CPU vs Parallel GPU | ~4–6 min |
| 008 | [008-lab-sequential-cpu-vs-parallel-gpu.md](002-gpu-fundamentals-from-silicon-to-cloud/008-lab-sequential-cpu-vs-parallel-gpu.md) | [Lab] Sequential CPU vs Parallel GPU | ~10–15 min |

### 003 — AWS Batch: Scaling GPU Workloads

| # | File | Title | Runtime |
|---|------|-------|---------|
| 000 | [000-what-is-aws-batch.md](003-aws-batch-scaling-gpu-workloads/000-what-is-aws-batch.md) | What Is AWS Batch? | ~2 min |
| 001 | [001-batch-vs-ec2-lambda-and-ecs.md](003-aws-batch-scaling-gpu-workloads/001-batch-vs-ec2-lambda-and-ecs.md) | Batch vs EC2, Lambda, and ECS | ~3 min |
| 002 | [002-core-building-blocks-of-aws-batch.md](003-aws-batch-scaling-gpu-workloads/002-core-building-blocks-of-aws-batch.md) | Core Building Blocks of AWS Batch | ~2 min |
| 003 | [003-compute-environments-ec2-fargate-and-eks.md](003-aws-batch-scaling-gpu-workloads/003-compute-environments-ec2-fargate-and-eks.md) | Compute Environments: EC2, Fargate, and EKS | ~2 min |
| 004 | [lessons/03-aws-batch-console/004-create-the-batch-control-plane.md](../lessons/03-aws-batch-console/004-create-the-batch-control-plane.md) | [Demo] Create the Batch control plane | console |
| 005 | [005-anatomy-of-a-job-definition.md](003-aws-batch-scaling-gpu-workloads/005-anatomy-of-a-job-definition.md) | Anatomy of a Job Definition | ~2 min |
| 006 | [lessons/03-aws-batch-console/006-job-definition-and-dummy-job.md](../lessons/03-aws-batch-console/006-job-definition-and-dummy-job.md) | [Demo] Job definition and dummy job | console |
| 007 | [007-how-batch-schedules-your-jobs.md](003-aws-batch-scaling-gpu-workloads/007-how-batch-schedules-your-jobs.md) | How Batch Schedules Your Jobs? | ~2 min |
| 008 | [008-array-jobs-and-job-dependencies.md](003-aws-batch-scaling-gpu-workloads/008-array-jobs-and-job-dependencies.md) | Array Jobs and Job Dependencies | ~2 min |
| 009 | [009-requesting-gpus-in-a-job-definition.md](003-aws-batch-scaling-gpu-workloads/009-requesting-gpus-in-a-job-definition.md) | Requesting GPUs in a Job Definition | ~2 min |
| 010 | [010-gpu-instance-types-for-batch.md](003-aws-batch-scaling-gpu-workloads/010-gpu-instance-types-for-batch.md) | GPU Instance Types for Batch | ~2 min |
| 011 | [011-gpu-ready-amis-and-containers.md](003-aws-batch-scaling-gpu-workloads/011-gpu-ready-amis-and-containers.md) | GPU-Ready AMIs and Containers | ~2 min |
| 012 | [012-multi-node-parallel-jobs-for-training.md](003-aws-batch-scaling-gpu-workloads/012-multi-node-parallel-jobs-for-training.md) | Multi-Node Parallel Jobs for Training | ~2 min |
| 013 | [013-cutting-gpu-costs-with-spot.md](003-aws-batch-scaling-gpu-workloads/013-cutting-gpu-costs-with-spot.md) | Cutting GPU Costs with Spot | ~2 min |
| 014 | [014-monitoring-batch-jobs-and-gpu-usage.md](003-aws-batch-scaling-gpu-workloads/014-monitoring-batch-jobs-and-gpu-usage.md) | Monitoring Batch Jobs and GPU Usage | ~2 min |
| 015 | [lessons/03-aws-batch-console/015-run-a-gpu-job-on-spot.md](../lessons/03-aws-batch-console/015-run-a-gpu-job-on-spot.md) | [Demo] Run a GPU job on Spot | console |

### 004 — Building the GPU Application

| # | File | Title | Runtime |
|---|------|-------|---------|
| 000 | [000-understanding-our-gpu-application.md](004-building-the-gpu-application/000-understanding-our-gpu-application.md) | Understanding Our GPU Application | ~2 min |
| 001 | [001-separating-storage-logic-from-gpu-processing.md](004-building-the-gpu-application/001-separating-storage-logic-from-gpu-processing.md) | Separating Storage Logic from GPU Processing | ~2 min |
| 003 | [003-how-gpu-inference-works-inside-the-application.md](004-building-the-gpu-application/003-how-gpu-inference-works-inside-the-application.md) | How GPU Inference Works Inside the Application | ~2 min |
| 004 | [004-understanding-gpu-micro-batching.md](004-building-the-gpu-application/004-understanding-gpu-micro-batching.md) | Understanding GPU Micro-Batching | ~2 min |
| 005 | [005-cuda-pytorch-and-nvidia-container-images.md](004-building-the-gpu-application/005-cuda-pytorch-and-nvidia-container-images.md) | CUDA, PyTorch and NVIDIA Container Images | ~2 min |
| 006 | [006-containerizing-gpu-applications-with-docker.md](004-building-the-gpu-application/006-containerizing-gpu-applications-with-docker.md) | Containerizing GPU Applications with Docker | ~2 min |

### 005 — Building the Data and Container Pipeline

| # | File | Title | Runtime |
|---|------|-------|---------|
| 000 | [000-why-gpu-containers-need-a-container-registry.md](005-building-the-data-and-container-pipeline/000-why-gpu-containers-need-a-container-registry.md) | Why GPU Containers Need a Container Registry | ~2 min |
| 001 | [001-amazon-ecr-repositories-tags-and-image-digests.md](005-building-the-data-and-container-pipeline/001-amazon-ecr-repositories-tags-and-image-digests.md) | Amazon ECR: Repositories, Tags and Image Digests | ~2 min |
| 005 | [005-designing-storage-for-batch-gpu-pipelines.md](005-building-the-data-and-container-pipeline/005-designing-storage-for-batch-gpu-pipelines.md) | Designing Storage for Batch GPU Pipelines | ~2 min |
| 006 | [006-amazon-s3-prefixes-as-the-input-output-contract.md](005-building-the-data-and-container-pipeline/006-amazon-s3-prefixes-as-the-input-output-contract.md) | Amazon S3 Prefixes as the Input/Output Contract | ~2 min |

### 006 — Building the AWS Batch GPU Infrastructure

| # | File | Title | Runtime |
|---|------|-------|---------|
| 000 | [000-aws-batch-compute-environments-explained.md](006-building-the-aws-batch-gpu-infrastructure/000-aws-batch-compute-environments-explained.md) | AWS Batch Compute Environments Explained | ~2 min |
| 001 | [001-how-aws-batch-finds-and-launches-gpu-capacity.md](006-building-the-aws-batch-gpu-infrastructure/001-how-aws-batch-finds-and-launches-gpu-capacity.md) | How AWS Batch Finds and Launches GPU Capacity | ~2 min |
| 002 | [002-nvidia-ecs-optimized-amis-and-gpu-drivers.md](006-building-the-aws-batch-gpu-infrastructure/002-nvidia-ecs-optimized-amis-and-gpu-drivers.md) | NVIDIA ECS-Optimized AMIs and GPU Drivers | ~2 min |
| 003 | [003-iam-roles-in-aws-batch.md](006-building-the-aws-batch-gpu-infrastructure/003-iam-roles-in-aws-batch.md) | IAM Roles in AWS Batch: Service, Instance and Job Roles | ~3 min |
| 004 | [004-networking-requirements-for-batch-gpu-jobs.md](006-building-the-aws-batch-gpu-infrastructure/004-networking-requirements-for-batch-gpu-jobs.md) | Networking Requirements for Batch GPU Jobs | ~2 min |
| 006 | [006-understanding-job-queues-and-scheduling.md](006-building-the-aws-batch-gpu-infrastructure/006-understanding-job-queues-and-scheduling.md) | Understanding Job Queues and Scheduling | ~2 min |
| 008 | [008-understanding-gpu-job-definitions.md](006-building-the-aws-batch-gpu-infrastructure/008-understanding-gpu-job-definitions.md) | Understanding GPU Job Definitions | ~3 min |

### 007 — Running the End-to-End GPU Pipeline

| # | File | Title | Runtime |
|---|------|-------|---------|
| 000 | [000-from-s3-input-to-gpu-job-following-the-execution-flow.md](007-running-the-end-to-end-gpu-pipeline/000-from-s3-input-to-gpu-job-following-the-execution-flow.md) | From S3 Input to GPU Job: Following the Execution Flow | ~2 min |
| 001 | [001-aws-batch-job-lifecycle-submitted-to-succeeded.md](007-running-the-end-to-end-gpu-pipeline/001-aws-batch-job-lifecycle-submitted-to-succeeded.md) | AWS Batch Job Lifecycle: Submitted to Succeeded | ~2 min |
| 003 | [003-understanding-container-overrides-and-runtime-parameters.md](007-running-the-end-to-end-gpu-pipeline/003-understanding-container-overrides-and-runtime-parameters.md) | Understanding Container Overrides and Runtime Parameters | ~2 min |
| 005 | [005-gpu-cold-starts-and-container-startup-time.md](007-running-the-end-to-end-gpu-pipeline/005-gpu-cold-starts-and-container-startup-time.md) | GPU Cold Starts and Container Startup Time | ~2 min |
| 006 | [006-understanding-runnable-jobs-and-gpu-capacity-problems.md](007-running-the-end-to-end-gpu-pipeline/006-understanding-runnable-jobs-and-gpu-capacity-problems.md) | Understanding RUNNABLE Jobs and GPU Capacity Problems | ~2 min |

### 008 — Production GPU Pipeline Design

| # | File | Title | Runtime |
|---|------|-------|---------|
| 000 | [000-reviewing-the-complete-production-architecture.md](008-production-gpu-pipeline-design/000-reviewing-the-complete-production-architecture.md) | Reviewing the Complete Production Architecture | ~2 min |
| 001 | [001-scaling-from-one-vendor-folder-to-thousands-of-jobs.md](008-production-gpu-pipeline-design/001-scaling-from-one-vendor-folder-to-thousands-of-jobs.md) | Scaling from One Vendor Folder to Thousands of Jobs | ~2 min |
| 002 | [002-parallelism-job-queues-and-gpu-utilization.md](008-production-gpu-pipeline-design/002-parallelism-job-queues-and-gpu-utilization.md) | Parallelism, Job Queues and GPU Utilization | ~2 min |
| 003 | [003-when-aws-batch-is-the-right-choice-and-when-it-isnt.md](008-production-gpu-pipeline-design/003-when-aws-batch-is-the-right-choice-and-when-it-isnt.md) | When AWS Batch Is the Right Choice — and When It Isn't | ~2 min |
| 004 | [004-aws-batch-vs-ecs-vs-eks-vs-sagemaker-for-gpu-workloads.md](008-production-gpu-pipeline-design/004-aws-batch-vs-ecs-vs-eks-vs-sagemaker-for-gpu-workloads.md) | AWS Batch vs ECS vs EKS vs SageMaker for GPU Workloads | ~3 min |
| 005 | [005-demo-final-end-to-end-pipeline-walkthrough.md](008-production-gpu-pipeline-design/005-demo-final-end-to-end-pipeline-walkthrough.md) | [Demo] Final End-to-End Pipeline Walkthrough | ~10–12 min |

### 009 — The Global GPU Landscape: Demand, Constraints & Regulations

| # | File | Title | Runtime |
|---|------|-------|---------|
| 000 | [000-why-gpus-have-become-critical-global-infrastructure.md](009-the-global-gpu-landscape-demand-constraints-regulations/000-why-gpus-have-become-critical-global-infrastructure.md) | Why GPUs Have Become Critical Global Infrastructure | ~2 min |
| 001 | [001-the-global-gpu-supply-chain-from-chip-design-to-cloud.md](009-the-global-gpu-landscape-demand-constraints-regulations/001-the-global-gpu-supply-chain-from-chip-design-to-cloud.md) | The Global GPU Supply Chain: From Chip Design to Cloud | ~2 min |
| 002 | [002-why-there-is-a-gpu-capacity-problem.md](009-the-global-gpu-landscape-demand-constraints-regulations/002-why-there-is-a-gpu-capacity-problem.md) | Why There Is a GPU Capacity Problem | ~2 min |
| 003 | [003-gpu-demand-ai-training-inference-and-the-cloud.md](009-the-global-gpu-landscape-demand-constraints-regulations/003-gpu-demand-ai-training-inference-and-the-cloud.md) | GPU Demand: AI Training, Inference and the Cloud | ~2 min |
| 004 | [004-the-nvidia-ecosystem-and-cudas-role-in-modern-ai.md](009-the-global-gpu-landscape-demand-constraints-regulations/004-the-nvidia-ecosystem-and-cudas-role-in-modern-ai.md) | The NVIDIA Ecosystem and CUDA's Role in Modern AI | ~2 min |
| 005 | [005-gpu-availability-across-aws-regions-and-cloud-providers.md](009-the-global-gpu-landscape-demand-constraints-regulations/005-gpu-availability-across-aws-regions-and-cloud-providers.md) | GPU Availability Across AWS Regions and Cloud Providers | ~2 min |
| 006 | [006-data-centers-power-cooling-and-the-physical-cost-of-ai.md](009-the-global-gpu-landscape-demand-constraints-regulations/006-data-centers-power-cooling-and-the-physical-cost-of-ai.md) | Data Centers, Power, Cooling and the Physical Cost of AI | ~2 min |
| 007 | [007-gpu-export-controls-trade-restrictions-and-geopolitics.md](009-the-global-gpu-landscape-demand-constraints-regulations/007-gpu-export-controls-trade-restrictions-and-geopolitics.md) | GPU Export Controls, Trade Restrictions and Geopolitics | ~2 min |
| 008 | [008-ai-regulations-and-what-they-mean-for-gpu-infrastructure.md](009-the-global-gpu-landscape-demand-constraints-regulations/008-ai-regulations-and-what-they-mean-for-gpu-infrastructure.md) | AI Regulations and What They Mean for GPU Infrastructure | ~2 min |
| 009 | [009-data-residency-sovereignty-and-running-ai-across-borders.md](009-the-global-gpu-landscape-demand-constraints-regulations/009-data-residency-sovereignty-and-running-ai-across-borders.md) | Data Residency, Sovereignty and Running AI Across Borders | ~2 min |
| 010 | [010-the-economics-of-gpus-why-gpu-compute-is-expensive.md](009-the-global-gpu-landscape-demand-constraints-regulations/010-the-economics-of-gpus-why-gpu-compute-is-expensive.md) | The Economics of GPUs: Why GPU Compute Is Expensive | ~2 min |
| 011 | [011-the-future-of-gpu-infrastructure.md](009-the-global-gpu-landscape-demand-constraints-regulations/011-the-future-of-gpu-infrastructure.md) | The Future of GPU Infrastructure: More GPUs or Better Efficiency? | ~3 min |
