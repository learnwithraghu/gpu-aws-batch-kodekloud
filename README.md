# Food catalog descriptions on AWS Batch

A vendor uploads one folder of dish photos (about 25–30). One GPU job writes one catalog CSV the food app can read. Each lesson adds one piece with the AWS CLI: the image, the registry, the buckets, the Batch environment, then the job.

```
s3://<images-bucket>/images/<batch>/
s3://<descriptions-bucket>/descriptions/<batch>/descriptions.csv
```

```csv
image_s3_uri,item_description
s3://<images-bucket>/images/vendor-a/bowl.jpg,a food dish of noodles with vegetables
```

Course outline: [syllabus.md](syllabus.md). Live queue, job definition, and bucket names: [`docs/aws-batch-setup.md`](docs/aws-batch-setup.md).

## Lessons

| # | Lesson | What you do |
|---|--------|-------------|
| [00](lessons/00-the-real-job/) | The real job | See the folder in, the one CSV out, and why it is a GPU batch job |
| [01](lessons/01-batch-and-gpu/) | AWS Batch and the GPU | Learn the compute environment, queue, job definition, and what a GPU job needs |
| [02](lessons/02-the-container-program/) | The container program | Read `photos.py` (S3) and `describe_items.py` (GPU) |
| [03](lessons/03-build-the-image/) | Build the image locally | `docker build --platform linux/amd64 -t gpu-teaching:latest .` |
| [04](lessons/04-push-to-ecr/) | Push to ECR | Create the repository, log in, tag, and push |
| [05](lessons/05-create-the-buckets/) | Create the buckets | `aws s3api create-bucket` for photos and the CSV |
| [06](lessons/06-upload-the-images/) | Upload the images | `aws s3 sync` one vendor folder to `images/<batch>/` |
| [07](lessons/07-the-batch-environment/) | The Batch environment | Create the GPU environment, queue, and job definition |
| [08](lessons/08-submit-the-job/) | Submit the job | `aws batch submit-job` for `images/sample/` |
| [09](lessons/09-read-the-catalog/) | Read the catalog | `aws s3 cp` the CSV |

After `photos.py`, `describe_items.py`, or the Dockerfile changes, build and push again (lessons 03 and 04). Batch runs the image in ECR.
