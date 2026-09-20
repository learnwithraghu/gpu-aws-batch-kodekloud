# GPU Image Captioning with AWS Batch

- **Course Description:** Build an image-captioning-to-vector-search pipeline using Docker, GPU instances, AWS Batch, Amazon S3, BLIP, CLIP, and S3 Vectors.
- **Audience:** Data scientists and Python developers who want to run batch inference workloads on GPUs.
- **Course Length:** 8 lessons
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
-  **[Lab] ->** Execute the notebook and compare timing results; use saved results when no local GPU is available
-  **[Deliverable] ->** A CPU-versus-GPU benchmark comparison and an explanation of when GPU acceleration is useful
  - **AWS Services:** None
  - **Estimated Time:** 45-60 minutes

- **Lesson 02: Your First AWS Batch GPU Job**
-  **[Video] ->** AWS Batch Compute Environments, Job Queues, Job Definitions, Jobs, and CloudWatch Logs
-  **[Demo] ->** Submit a container to a g4dn.xlarge (NVIDIA T4) GPU environment and inspect GPU benchmark logs
-  **[Lab] ->** Run the notebook, poll the job to completion, and inspect the CloudWatch log stream
-  **[Deliverable] ->** A successful AWS Batch GPU job with verified GPU model, memory, and runtime output
  - **AWS Services:** AWS Batch, Amazon ECR
  - **Estimated Time:** 45-60 minutes

- **Lesson 03: Images to Captions**
-  **[Video] ->** Image Captioning, BLIP, and the S3-to-Batch I/O Pattern
-  **[Demo] ->** Upload a folder of sample images, generate captions in a Batch GPU job, and display images with their captions
-  **[Lab] ->** Run submit_job.py, caption the sample images, and write the caption manifest back to S3
-  **[Deliverable] ->** A caption manifest stored in S3 and an understanding of Batch input/output flow
  - **AWS Services:** AWS Batch, Amazon S3
  - **Estimated Time:** 60-75 minutes

- **Lesson 04: Captions to Embeddings**
-  **[Video] ->** CLIP, Text Embeddings, GPU Batching, Normalized Vectors, and Inference Throughput
-  **[Demo] ->** Load CLIP's text encoder, embed captions in batches of 16, and report GPU speedup
-  **[Lab] ->** Generate embeddings for the generated captions and upsert them into S3 Vectors
-  **[Deliverable] ->** Caption embeddings and metadata stored in the S3 Vectors index
  - **AWS Services:** AWS Batch, Amazon S3
  - **Estimated Time:** 60-90 minutes

- **Lesson 05: Vector Search**
-  **[Video] ->** Embeddings, Cosine Similarity, Nearest-Neighbor Search, and Semantic Retrieval
-  **[Demo] ->** Encode a text query and use S3 Vectors to return the top matching captioned images
-  **[Lab] ->** Search queries such as a dog playing in a park, retrieve matching S3 images, and inspect the results
-  **[Deliverable] ->** Top matching images with similarity results and metadata
  - **AWS Services:** Amazon S3, S3 Vectors
  - **Estimated Time:** 45-60 minutes

- **Lesson 06: The Full Pipeline**
-  **[Video] ->** Production Pipelines, DAGs, Job Dependencies, and Failure Handling
-  **[Demo] ->** Submit captioning and embedding jobs together using AWS Batch dependsOn
-  **[Lab] ->** Run run_pipeline.py, monitor both jobs, and verify the final embeddings in S3 Vectors
-  **[Deliverable] ->** A working image-to-embeddings pipeline with dependent-job orchestration
  - **AWS Services:** AWS Batch, Amazon S3
  - **Estimated Time:** 60-75 minutes

- **Lesson 07: Scale and Cost**
-  **[Video] ->** Batch Array Jobs, Spot Pricing, Throughput, Cost per Unit, and GPU-vs-CPU Decisions
-  **[Demo] ->** Fan one submission out to multiple parallel jobs and review the cost model
-  **[Lab] ->** Run an array job, vary the array size, and estimate cost and wall-clock time for multiple image batches
-  **[Deliverable] ->** A scaling and cost estimate for processing a batch of image batches
  - **AWS Services:** AWS Batch, Amazon S3
  - **Estimated Time:** 45-60 minutes
