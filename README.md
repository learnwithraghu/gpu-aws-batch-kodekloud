# Food item descriptions on AWS Batch

Vendors upload food photos (about 25–30 at a time) to the images bucket:

```
s3://<images-bucket>/images/<batch>/
```

A GPU job writes one item description per photo for the food app:

```
s3://<descriptions-bucket>/descriptions/<batch>/descriptions.csv
```

```csv
image_s3_uri,item_description
s3://<images-bucket>/images/vendor-a/bowl.jpg,a food dish of noodles with vegetables
```

Live queue, job definition, and bucket names: [`docs/aws-batch-setup.md`](docs/aws-batch-setup.md).

## Scripts

| Script | Where it runs | What it does |
|--------|----------------|--------------|
| `describe_items.py` | Inside the GPU container | Read the image folder, write the CSV |
| `register_job_def.py` | Your laptop | Point Batch at the ECR image |
| `submit_job.py` | Your laptop | Submit one folder and wait |
| `show_descriptions.py` | Your laptop | Print the CSV |

```bash
python register_job_def.py
python submit_job.py --batch-stem vendor-a
python show_descriptions.py --batch-stem vendor-a
```

After `describe_items.py` or the Dockerfile changes, rebuild the image Batch actually runs:

```bash
bash helpers/push_ecr_image.sh
```
