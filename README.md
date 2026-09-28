# Food catalog descriptions on AWS Batch

A vendor uploads one folder of dish photos (about 25–30). One GPU job writes one catalog CSV the food app can read.

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
| [00](lessons/00-the-catalog/) | The catalog | See the folder in and the one CSV out |
| [01](lessons/01-create-the-buckets/) | Create the buckets | `bash helpers/setup_infra.sh up` |
| [02](lessons/02-upload-the-images/) | Upload the images | Sync one vendor folder to `images/<batch>/` |
| [03](lessons/03-the-job-script/) | The job script | Read `describe_items.py` |
| [04](lessons/04-the-image/) | The image | See what Batch actually runs |
| [05](lessons/05-register-the-job/) | Register the job | `python register_job_def.py` |
| [06](lessons/06-submit-and-wait/) | Submit and wait | `python submit_job.py --batch-stem sample` |
| [07](lessons/07-read-the-catalog/) | Read the catalog | `python show_descriptions.py --batch-stem sample` |

After `describe_items.py` or the Dockerfile changes, rebuild the image Batch runs:

```bash
bash helpers/push_ecr_image.sh
```
