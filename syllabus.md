# Food Catalog Descriptions with AWS Batch

- **Course Description:** Turn a vendor folder of dish photos into one food-catalog CSV. Build the GPU image, push it to ECR, create the buckets, stand up an AWS Batch GPU environment, and submit one job with the AWS CLI.
- **Audience:** Python developers who want to run a real GPU job on AWS Batch, one CLI step at a time.
- **Course Length:** 10 lessons
- **Reference Region:** ap-northeast-1 (Tokyo)

## Course Syllabus

- **Lesson 00: The Real Job**
-  **[Video] ->** A vendor folder of dish photos, one catalog CSV, and why the GPU should not stay on between drops
-  **[Demo] ->** Walk the input prefix and the output file, one row per photo
-  **[Lab] ->** Read this lesson only. No AWS commands
-  **[Deliverable] ->** You can point at `images/<batch>/` and `descriptions/<batch>/descriptions.csv` and say why this is a batch GPU job
  - **AWS Services:** None
  - **Estimated Time:** 15 minutes

- **Lesson 01: AWS Batch and the GPU**
-  **[Video] ->** Compute environment, job queue, job definition, and job — and what changes when the job needs a GPU
-  **[Demo] ->** `g4dn.xlarge`, the NVIDIA AMI, 1 GPU, 12288 MiB, the instance role versus the job role, Spot versus on-demand
-  **[Lab] ->** Describe the live environment, queue, and job definition. Create nothing
-  **[Deliverable] ->** You can name the four Batch objects and say why 16384 MiB never places
  - **AWS Services:** AWS Batch
  - **Estimated Time:** 25 minutes

- **Lesson 02: The Container Program**
-  **[Video] ->** Two files: `photos.py` talks to S3, `describe_items.py` talks to the GPU
-  **[Demo] ->** List the folder, describe groups of 8, write one CSV
-  **[Lab] ->** Read `photos.py`, then `describe_items.py`. Do not submit a job
-  **[Deliverable] ->** You can explain that 8-at-a-time is GPU memory, and that these files do not create AWS resources
  - **AWS Services:** None
  - **Estimated Time:** 20 minutes

- **Lesson 03: Build the Image Locally**
-  **[Video] ->** The Dockerfile: PyTorch CUDA base, pinned transformers, one copied program
-  **[Demo] ->** `docker build --platform linux/amd64 -t gpu-teaching:latest .`
-  **[Lab] ->** Build the image and confirm the local tag with `docker images`
-  **[Deliverable] ->** A local `gpu-teaching:latest` image. Nothing pushed yet
  - **AWS Services:** None
  - **Estimated Time:** 25 minutes

- **Lesson 04: Push to ECR**
-  **[Video] ->** Create the repository, log Docker in, tag, and push `:latest`
-  **[Demo] ->** `aws ecr create-repository`, `aws ecr get-login-password`, `docker push`
-  **[Lab] ->** Push `gpu-teaching:latest` and write `ECR_IMAGE_URI` into `.env`
-  **[Deliverable] ->** `aws ecr describe-images` shows the `latest` tag
  - **AWS Services:** Amazon ECR
  - **Estimated Time:** 25 minutes

- **Lesson 05: Create the Buckets**
-  **[Video] ->** The images bucket and the CSV bucket, created with the AWS CLI
-  **[Demo] ->** `aws s3api create-bucket` with a location constraint, then the names written to `.env`
-  **[Lab] ->** Create both buckets (or confirm they exist) and set `S3_BUCKET`, `S3_IMAGES_BUCKET`, and `S3_CSV_BUCKET`
-  **[Deliverable] ->** Both buckets listed by `aws s3 ls`, names recorded in `.env`
  - **AWS Services:** Amazon S3
  - **Estimated Time:** 15 minutes

- **Lesson 06: Upload the Images**
-  **[Video] ->** Where a vendor batch lives: `images/<batch>/`, about 25–30 jpg, jpeg, or png photos
-  **[Demo] ->** `aws s3 sync` into that prefix
-  **[Lab] ->** Upload one folder and list it
-  **[Deliverable] ->** Every photo for the batch is under `images/<batch>/`
  - **AWS Services:** Amazon S3
  - **Estimated Time:** 15 minutes

- **Lesson 07: The Batch Environment**
-  **[Video] ->** Instance role, job role, GPU compute environment, queue, and job definition
-  **[Demo] ->** `aws batch create-compute-environment`, `create-job-queue`, and `register-job-definition` (12288 MiB, 1 GPU, job role)
-  **[Lab] ->** Describe each piece. Create it only if it is missing. Record the queue and job definition in `.env`
-  **[Deliverable] ->** Spot environment and queue `VALID`. Active job definition is revision `:3` or later. Do not use `:1` or `:2`
  - **AWS Services:** AWS Batch, IAM
  - **Estimated Time:** 30 minutes

- **Lesson 08: Submit the Job**
-  **[Video] ->** One `submit-job` for one folder, polled until the job finishes
-  **[Demo] ->** `aws batch submit-job` with a container override, then `describe-jobs`
-  **[Lab] ->** Submit `images/sample/` and wait for `SUCCEEDED`. If it stays `RUNNABLE`, resubmit on the on-demand queue
-  **[Deliverable] ->** One catalog file at `descriptions/sample/descriptions.csv`
  - **AWS Services:** AWS Batch, Amazon S3
  - **Estimated Time:** 25 minutes

- **Lesson 09: Read the Catalog**
-  **[Video] ->** The CSV the food app reads: description and image URI on each row
-  **[Demo] ->** `aws s3 cp` of `descriptions/sample/descriptions.csv`
-  **[Lab] ->** Print the sample catalog and confirm one header plus one row per photo
-  **[Deliverable] ->** The CSV printed locally, row count matching the uploaded photos
  - **AWS Services:** Amazon S3
  - **Estimated Time:** 15 minutes
