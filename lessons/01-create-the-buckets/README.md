# Lesson 01 — Create the buckets

Two buckets. One holds the vendor photos. The other holds the catalog CSV.

## Two buckets

| Bucket | Role |
|--------|------|
| Images | `images/<batch>/` dish photos |
| CSV | `descriptions/<batch>/descriptions.csv` |

The live CSV bucket name still contains `captions`. That name stays. New files use the `descriptions/` prefix inside it.

## The command

From the repo root, with the AWS CLI already configured:

```bash
bash helpers/setup_infra.sh up
```

This calls `helpers/create_buckets.sh`. A second run skips buckets that already exist. It does not empty them.

## What lands in `.env`

The script writes:

- `S3_IMAGES_BUCKET` — the images bucket
- `S3_CSV_BUCKET` — the catalog CSV bucket
- `S3_BUCKET` — the same value as the images bucket

Later lessons and `submit_job.py` read these names from `.env`. Do not commit `.env`.

## Check

```bash
aws s3 ls
```

You should see both buckets. The names match the three variables in `.env`.
