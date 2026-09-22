# GPU Image Captioning with AWS Batch

- **Course Description:** Build an image-captioning pipeline on AWS Batch — Dockerize GPU workloads, run BLIP captioning jobs on Amazon EC2 GPU Spot instances, and store image captions (with their S3 image links) in Amazon S3.
- **Audience:** Data scientists and Python developers who want to run batch inference workloads on GPUs.
- **Course Length:** 6 lessons
- **Reference Region:** ap-northeast-1 (Tokyo)

## Course Syllabus

- **Lesson 00: Build and Push the GPU Docker Image**
-  **[Video] ->** Containerizing GPU Workloads with Docker, CUDA, and Amazon ECR
-  **[Demo] ->** Inspect the Dockerfile, authenticate to ECR, build the image, tag it, and push it
-  **[Lab] ->** Create the ECR repository, build the shared course image, push it, and configure the image URI
-  **[Deliverable] ->** A versioned GPU Docker image in ECR and an understanding of repeatable CUDA environments
  - **AWS Services:** Amazon ECR
  - **Estimated Time:** 60-90 minutes

- **Lesson 01: Why GPU?**
-  **[Video] ->** CPU vs GPU Architecture, Parallelism, Tensors, and Matrix Multiplication
-  **[Demo] ->** Run the same PyTorch matrix multiplication on CPU and GPU across multiple matrix sizes
-  **[Lab] ->** Run benchmark_gpu.py locally and compare the timing table; reference T4 results are used when no local GPU is available
-  **[Deliverable] ->** A CPU-versus-GPU benchmark comparison and an explanation of when GPU acceleration is useful
  - **AWS Services:** None
  - **Estimated Time:** 45-60 minutes

- **Lesson 02: Your First AWS Batch GPU Job**
-  **[Video] ->** AWS Batch Compute Environments, Job Queues, Job Definitions, Jobs, and CloudWatch Logs
-  **[Demo] ->** Submit a container to a g4dn.xlarge (NVIDIA T4) GPU environment and inspect GPU benchmark logs
-  **[Lab] ->** Run submit_job.py, poll the job to completion, and inspect the CloudWatch log stream
-  **[Deliverable] ->** A successful AWS Batch GPU job with verified GPU model, memory, and runtime output
  - **AWS Services:** AWS Batch, Amazon ECR
  - **Estimated Time:** 45-60 minutes

- **Lesson 03: Images to Captions**
-  **[Video] ->** Image Captioning, BLIP, and the S3-to-Batch I/O Pattern
-  **[Demo] ->** Upload a folder of sample images, generate captions in a Batch GPU job, and print the caption table
-  **[Lab] ->** Run submit_job.py to caption the sample images, then show_captions.py to review the results
-  **[Deliverable] ->** A caption file in S3 (one row per image: S3 image URI + caption) and an understanding of the Batch input/output flow
  - **AWS Services:** AWS Batch, Amazon S3
  - **Estimated Time:** 60-75 minutes

- **Lesson 04: The Full Pipeline**
-  **[Video] ->** Production Pipelines, DAGs, Job Dependencies, and Failure Handling
-  **[Demo] ->** Submit captioning and verification jobs together using AWS Batch dependsOn
-  **[Lab] ->** Run run_pipeline.py, monitor both jobs, and confirm the _VERIFIED marker in S3
-  **[Deliverable] ->** A working image-to-caption pipeline with dependent-job orchestration
  - **AWS Services:** AWS Batch, Amazon S3
  - **Estimated Time:** 60-75 minutes

- **Lesson 05: Scale and Cost**
-  **[Video] ->** Batch Array Jobs, Spot Pricing, Throughput, Cost per Unit, and GPU-vs-CPU Decisions
-  **[Demo] ->** Fan one submission out to multiple parallel jobs and review the cost model
-  **[Lab] ->** Run an array job, vary the array size, and estimate cost and wall-clock time for multiple image batches
-  **[Deliverable] ->** A scaling and cost estimate for processing a batch of image batches
  - **AWS Services:** AWS Batch, Amazon S3
  - **Estimated Time:** 45-60 minutes
