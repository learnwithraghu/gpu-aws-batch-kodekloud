# Food Catalog Descriptions with AWS Batch

- **Course Description:** Turn a vendor folder of dish photos into one food-catalog CSV. Create the S3 buckets, upload the photos, and run one GPU job on AWS Batch that writes a short catalog description for every image.
- **Audience:** Python developers who want to run one batch inference job over a folder of images.
- **Course Length:** 8 lessons
- **Reference Region:** ap-northeast-1 (Tokyo)

## Course Syllabus

- **Lesson 00: The Catalog**
-  **[Video] ->** A vendor folder of dish photos and the one CSV the food app reads
-  **[Demo] ->** Walk the input prefix and the output file, one row per photo
-  **[Lab] ->** Read this lesson only. No AWS commands
-  **[Deliverable] ->** You can point at `images/<batch>/` and `descriptions/<batch>/descriptions.csv` and say what each row means
  - **AWS Services:** None
  - **Estimated Time:** 15 minutes

- **Lesson 01: Create the Buckets**
-  **[Video] ->** The images bucket and the CSV bucket, and why a second run does not recreate them
-  **[Demo] ->** `bash helpers/setup_infra.sh up` and the names written to `.env`
-  **[Lab] ->** Run the setup command and confirm both bucket names in `.env`
-  **[Deliverable] ->** `S3_BUCKET`, `S3_IMAGES_BUCKET`, and `S3_CSV_BUCKET` set in `.env`
  - **AWS Services:** Amazon S3
  - **Estimated Time:** 20 minutes

- **Lesson 02: Upload the Images**
-  **[Video] ->** Where a vendor batch lives: `images/<batch>/`, about 25–30 jpg, jpeg, or png photos
-  **[Demo] ->** `aws s3 sync` into that prefix, and `helpers/organize_uploads.sh` if files landed at the bucket root
-  **[Lab] ->** Upload one folder and list it
-  **[Deliverable] ->** Every photo for the batch is under `images/<batch>/`
  - **AWS Services:** Amazon S3
  - **Estimated Time:** 20 minutes

- **Lesson 03: The Job Script**
-  **[Video] ->** How `describe_items.py` lists the folder, describes photos on the GPU, and writes one CSV
-  **[Demo] ->** Read the script: environment variables, the file types, groups of 8, one `put_object` at the end
-  **[Lab] ->** Read `describe_items.py`. No job is submitted
-  **[Deliverable] ->** You can explain that 8-at-a-time is GPU memory, not extra CSV files
  - **AWS Services:** None
  - **Estimated Time:** 20 minutes

- **Lesson 04: The Image**
-  **[Video] ->** Batch runs the ECR image, not the file on your laptop
-  **[Demo] ->** Read the Dockerfile and `helpers/push_ecr_image.sh`
-  **[Lab] ->** Find `/app/describe_items.py` in the Dockerfile and the command that rebuilds `:latest`
-  **[Deliverable] ->** You know to rebuild after `describe_items.py` or the Dockerfile changes
  - **AWS Services:** Amazon ECR
  - **Estimated Time:** 20 minutes

- **Lesson 05: Register the Job**
-  **[Video] ->** The job definition: image, 4 vCPU, 12288 MiB, 1 GPU, and the S3 job role
-  **[Demo] ->** `python lessons/05-register-the-job/register_job_def.py`, including a second run that prints "already matches"
-  **[Lab] ->** Register and note the revision
-  **[Deliverable] ->** Active revision `:3` or later. Do not use `:1` or `:2`
  - **AWS Services:** AWS Batch
  - **Estimated Time:** 20 minutes

- **Lesson 06: Submit and Wait**
-  **[Video] ->** One submission for one folder, polled until the job finishes
-  **[Demo] ->** `python lessons/06-submit-and-wait/submit_job.py --batch-stem sample` and the status path
-  **[Lab] ->** Submit the sample folder and wait for SUCCEEDED
-  **[Deliverable] ->** One catalog file at `descriptions/sample/descriptions.csv`
  - **AWS Services:** AWS Batch, Amazon S3
  - **Estimated Time:** 25 minutes

- **Lesson 07: Read the Catalog**
-  **[Video] ->** The CSV the food app reads: description first, image URI under it
-  **[Demo] ->** `python lessons/07-read-the-catalog/show_descriptions.py --batch-stem sample`
-  **[Lab] ->** Print the sample catalog and open the same object in S3
-  **[Deliverable] ->** One header plus one row per photo
  - **AWS Services:** Amazon S3
  - **Estimated Time:** 15 minutes
