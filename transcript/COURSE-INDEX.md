# Course transcript index

Course: **Building Production GPU Workloads on AWS**

Source of truth: [`Building Production GPU Workloads on AWS - Draft-Raghu.csv`](../Building%20Production%20GPU%20Workloads%20on%20AWS%20-%20Draft-Raghu.csv). Video scripts are the default. Demo/Lab runbooks are included where drafted (Section 001 manual verification demo/lab; Section 007 final pipeline walkthrough). Two Section 001 stubs still need full scripts (`000` course approach, `006` whiteboard).

**Voice:** conversational teleprompter scripts for slide generation. Target **~2 minutes** (about 260–300 words) unless a topic needs **~3 minutes** (up to ~450 words).

**Structure:** `transcript/<section-folder>/<lecture#>-<slug>.md`

| Section | Folder | Videos (sheet) |
|---------|--------|----------------|
| 001 | [001-the-real-world-gpu-problem](001-the-real-world-gpu-problem/) | 4 (+ whiteboard; Demo/Lab separate) |
| 002 | [002-gpu-fundamentals-from-silicon-to-cloud](002-gpu-fundamentals-from-silicon-to-cloud/) | 6 |
| 003 | [003-building-the-gpu-application](003-building-the-gpu-application/) | 6 |
| 004 | [004-building-the-data-and-container-pipeline](004-building-the-data-and-container-pipeline/) | 4 |
| 005 | [005-building-the-aws-batch-gpu-infrastructure](005-building-the-aws-batch-gpu-infrastructure/) | 7 |
| 006 | [006-running-the-end-to-end-gpu-pipeline](006-running-the-end-to-end-gpu-pipeline/) | 5 |
| 007 | [007-production-gpu-pipeline-design](007-production-gpu-pipeline-design/) | 5 |
| 008 | [008-the-global-gpu-landscape-demand-constraints-regulations](008-the-global-gpu-landscape-demand-constraints-regulations/) | 12 |

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

### 003 — Building the GPU Application

| # | File | Title | Runtime |
|---|------|-------|---------|
| 000 | [000-understanding-our-gpu-application.md](003-building-the-gpu-application/000-understanding-our-gpu-application.md) | Understanding Our GPU Application | ~2 min |
| 001 | [001-separating-storage-logic-from-gpu-processing.md](003-building-the-gpu-application/001-separating-storage-logic-from-gpu-processing.md) | Separating Storage Logic from GPU Processing | ~2 min |
| 003 | [003-how-gpu-inference-works-inside-the-application.md](003-building-the-gpu-application/003-how-gpu-inference-works-inside-the-application.md) | How GPU Inference Works Inside the Application | ~2 min |
| 004 | [004-understanding-gpu-micro-batching.md](003-building-the-gpu-application/004-understanding-gpu-micro-batching.md) | Understanding GPU Micro-Batching | ~2 min |
| 005 | [005-cuda-pytorch-and-nvidia-container-images.md](003-building-the-gpu-application/005-cuda-pytorch-and-nvidia-container-images.md) | CUDA, PyTorch and NVIDIA Container Images | ~2 min |
| 006 | [006-containerizing-gpu-applications-with-docker.md](003-building-the-gpu-application/006-containerizing-gpu-applications-with-docker.md) | Containerizing GPU Applications with Docker | ~2 min |

### 004 — Building the Data and Container Pipeline

| # | File | Title | Runtime |
|---|------|-------|---------|
| 000 | [000-why-gpu-containers-need-a-container-registry.md](004-building-the-data-and-container-pipeline/000-why-gpu-containers-need-a-container-registry.md) | Why GPU Containers Need a Container Registry | ~2 min |
| 001 | [001-amazon-ecr-repositories-tags-and-image-digests.md](004-building-the-data-and-container-pipeline/001-amazon-ecr-repositories-tags-and-image-digests.md) | Amazon ECR: Repositories, Tags and Image Digests | ~2 min |
| 005 | [005-designing-storage-for-batch-gpu-pipelines.md](004-building-the-data-and-container-pipeline/005-designing-storage-for-batch-gpu-pipelines.md) | Designing Storage for Batch GPU Pipelines | ~2 min |
| 006 | [006-amazon-s3-prefixes-as-the-input-output-contract.md](004-building-the-data-and-container-pipeline/006-amazon-s3-prefixes-as-the-input-output-contract.md) | Amazon S3 Prefixes as the Input/Output Contract | ~2 min |

### 005 — Building the AWS Batch GPU Infrastructure

| # | File | Title | Runtime |
|---|------|-------|---------|
| 000 | [000-aws-batch-compute-environments-explained.md](005-building-the-aws-batch-gpu-infrastructure/000-aws-batch-compute-environments-explained.md) | AWS Batch Compute Environments Explained | ~2 min |
| 001 | [001-how-aws-batch-finds-and-launches-gpu-capacity.md](005-building-the-aws-batch-gpu-infrastructure/001-how-aws-batch-finds-and-launches-gpu-capacity.md) | How AWS Batch Finds and Launches GPU Capacity | ~2 min |
| 002 | [002-nvidia-ecs-optimized-amis-and-gpu-drivers.md](005-building-the-aws-batch-gpu-infrastructure/002-nvidia-ecs-optimized-amis-and-gpu-drivers.md) | NVIDIA ECS-Optimized AMIs and GPU Drivers | ~2 min |
| 003 | [003-iam-roles-in-aws-batch.md](005-building-the-aws-batch-gpu-infrastructure/003-iam-roles-in-aws-batch.md) | IAM Roles in AWS Batch: Service, Instance and Job Roles | ~3 min |
| 004 | [004-networking-requirements-for-batch-gpu-jobs.md](005-building-the-aws-batch-gpu-infrastructure/004-networking-requirements-for-batch-gpu-jobs.md) | Networking Requirements for Batch GPU Jobs | ~2 min |
| 006 | [006-understanding-job-queues-and-scheduling.md](005-building-the-aws-batch-gpu-infrastructure/006-understanding-job-queues-and-scheduling.md) | Understanding Job Queues and Scheduling | ~2 min |
| 008 | [008-understanding-gpu-job-definitions.md](005-building-the-aws-batch-gpu-infrastructure/008-understanding-gpu-job-definitions.md) | Understanding GPU Job Definitions | ~3 min |

### 006 — Running the End-to-End GPU Pipeline

| # | File | Title | Runtime |
|---|------|-------|---------|
| 000 | [000-from-s3-input-to-gpu-job-following-the-execution-flow.md](006-running-the-end-to-end-gpu-pipeline/000-from-s3-input-to-gpu-job-following-the-execution-flow.md) | From S3 Input to GPU Job: Following the Execution Flow | ~2 min |
| 001 | [001-aws-batch-job-lifecycle-submitted-to-succeeded.md](006-running-the-end-to-end-gpu-pipeline/001-aws-batch-job-lifecycle-submitted-to-succeeded.md) | AWS Batch Job Lifecycle: Submitted to Succeeded | ~2 min |
| 003 | [003-understanding-container-overrides-and-runtime-parameters.md](006-running-the-end-to-end-gpu-pipeline/003-understanding-container-overrides-and-runtime-parameters.md) | Understanding Container Overrides and Runtime Parameters | ~2 min |
| 005 | [005-gpu-cold-starts-and-container-startup-time.md](006-running-the-end-to-end-gpu-pipeline/005-gpu-cold-starts-and-container-startup-time.md) | GPU Cold Starts and Container Startup Time | ~2 min |
| 006 | [006-understanding-runnable-jobs-and-gpu-capacity-problems.md](006-running-the-end-to-end-gpu-pipeline/006-understanding-runnable-jobs-and-gpu-capacity-problems.md) | Understanding RUNNABLE Jobs and GPU Capacity Problems | ~2 min |

### 007 — Production GPU Pipeline Design

| # | File | Title | Runtime |
|---|------|-------|---------|
| 000 | [000-reviewing-the-complete-production-architecture.md](007-production-gpu-pipeline-design/000-reviewing-the-complete-production-architecture.md) | Reviewing the Complete Production Architecture | ~2 min |
| 001 | [001-scaling-from-one-vendor-folder-to-thousands-of-jobs.md](007-production-gpu-pipeline-design/001-scaling-from-one-vendor-folder-to-thousands-of-jobs.md) | Scaling from One Vendor Folder to Thousands of Jobs | ~2 min |
| 002 | [002-parallelism-job-queues-and-gpu-utilization.md](007-production-gpu-pipeline-design/002-parallelism-job-queues-and-gpu-utilization.md) | Parallelism, Job Queues and GPU Utilization | ~2 min |
| 003 | [003-when-aws-batch-is-the-right-choice-and-when-it-isnt.md](007-production-gpu-pipeline-design/003-when-aws-batch-is-the-right-choice-and-when-it-isnt.md) | When AWS Batch Is the Right Choice — and When It Isn't | ~2 min |
| 004 | [004-aws-batch-vs-ecs-vs-eks-vs-sagemaker-for-gpu-workloads.md](007-production-gpu-pipeline-design/004-aws-batch-vs-ecs-vs-eks-vs-sagemaker-for-gpu-workloads.md) | AWS Batch vs ECS vs EKS vs SageMaker for GPU Workloads | ~3 min |
| 005 | [005-demo-final-end-to-end-pipeline-walkthrough.md](007-production-gpu-pipeline-design/005-demo-final-end-to-end-pipeline-walkthrough.md) | [Demo] Final End-to-End Pipeline Walkthrough | ~10–12 min |

### 008 — The Global GPU Landscape: Demand, Constraints & Regulations

| # | File | Title | Runtime |
|---|------|-------|---------|
| 000 | [000-why-gpus-have-become-critical-global-infrastructure.md](008-the-global-gpu-landscape-demand-constraints-regulations/000-why-gpus-have-become-critical-global-infrastructure.md) | Why GPUs Have Become Critical Global Infrastructure | ~2 min |
| 001 | [001-the-global-gpu-supply-chain-from-chip-design-to-cloud.md](008-the-global-gpu-landscape-demand-constraints-regulations/001-the-global-gpu-supply-chain-from-chip-design-to-cloud.md) | The Global GPU Supply Chain: From Chip Design to Cloud | ~2 min |
| 002 | [002-why-there-is-a-gpu-capacity-problem.md](008-the-global-gpu-landscape-demand-constraints-regulations/002-why-there-is-a-gpu-capacity-problem.md) | Why There Is a GPU Capacity Problem | ~2 min |
| 003 | [003-gpu-demand-ai-training-inference-and-the-cloud.md](008-the-global-gpu-landscape-demand-constraints-regulations/003-gpu-demand-ai-training-inference-and-the-cloud.md) | GPU Demand: AI Training, Inference and the Cloud | ~2 min |
| 004 | [004-the-nvidia-ecosystem-and-cudas-role-in-modern-ai.md](008-the-global-gpu-landscape-demand-constraints-regulations/004-the-nvidia-ecosystem-and-cudas-role-in-modern-ai.md) | The NVIDIA Ecosystem and CUDA's Role in Modern AI | ~2 min |
| 005 | [005-gpu-availability-across-aws-regions-and-cloud-providers.md](008-the-global-gpu-landscape-demand-constraints-regulations/005-gpu-availability-across-aws-regions-and-cloud-providers.md) | GPU Availability Across AWS Regions and Cloud Providers | ~2 min |
| 006 | [006-data-centers-power-cooling-and-the-physical-cost-of-ai.md](008-the-global-gpu-landscape-demand-constraints-regulations/006-data-centers-power-cooling-and-the-physical-cost-of-ai.md) | Data Centers, Power, Cooling and the Physical Cost of AI | ~2 min |
| 007 | [007-gpu-export-controls-trade-restrictions-and-geopolitics.md](008-the-global-gpu-landscape-demand-constraints-regulations/007-gpu-export-controls-trade-restrictions-and-geopolitics.md) | GPU Export Controls, Trade Restrictions and Geopolitics | ~2 min |
| 008 | [008-ai-regulations-and-what-they-mean-for-gpu-infrastructure.md](008-the-global-gpu-landscape-demand-constraints-regulations/008-ai-regulations-and-what-they-mean-for-gpu-infrastructure.md) | AI Regulations and What They Mean for GPU Infrastructure | ~2 min |
| 009 | [009-data-residency-sovereignty-and-running-ai-across-borders.md](008-the-global-gpu-landscape-demand-constraints-regulations/009-data-residency-sovereignty-and-running-ai-across-borders.md) | Data Residency, Sovereignty and Running AI Across Borders | ~2 min |
| 010 | [010-the-economics-of-gpus-why-gpu-compute-is-expensive.md](008-the-global-gpu-landscape-demand-constraints-regulations/010-the-economics-of-gpus-why-gpu-compute-is-expensive.md) | The Economics of GPUs: Why GPU Compute Is Expensive | ~2 min |
| 011 | [011-the-future-of-gpu-infrastructure.md](008-the-global-gpu-landscape-demand-constraints-regulations/011-the-future-of-gpu-infrastructure.md) | The Future of GPU Infrastructure: More GPUs or Better Efficiency? | ~3 min |
