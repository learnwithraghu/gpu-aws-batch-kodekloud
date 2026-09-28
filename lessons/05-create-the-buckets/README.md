# Lesson 05 — Create the buckets

Two buckets. Photos go in one. The catalog CSV goes in the other. Names end with your account ID so they do not collide with another account.

Theory reading: [`theory.md`](theory.md).

```bash
export AWS_DEFAULT_REGION=ap-northeast-1
export ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export S3_IMAGES_BUCKET="gpu-teaching-images-${ACCOUNT_ID}"
export S3_CSV_BUCKET="gpu-teaching-captions-csv-${ACCOUNT_ID}"
```

The CSV bucket name still says `captions`. That is the live bucket. New files use the `descriptions/` prefix inside it.

## Create

`ap-northeast-1` requires a location constraint. A second run of `create-bucket` on a name you already own fails; check first.

```bash
aws s3api head-bucket --bucket "$S3_IMAGES_BUCKET" 2>/dev/null \
  || aws s3api create-bucket \
       --bucket "$S3_IMAGES_BUCKET" \
       --region "$AWS_DEFAULT_REGION" \
       --create-bucket-configuration "LocationConstraint=${AWS_DEFAULT_REGION}"

aws s3api head-bucket --bucket "$S3_CSV_BUCKET" 2>/dev/null \
  || aws s3api create-bucket \
       --bucket "$S3_CSV_BUCKET" \
       --region "$AWS_DEFAULT_REGION" \
       --create-bucket-configuration "LocationConstraint=${AWS_DEFAULT_REGION}"
```

## Check, and write `.env`

```bash
aws s3 ls | grep gpu-teaching
```

Add these lines to `.env` (same names you just created):

```bash
AWS_DEFAULT_REGION=ap-northeast-1
S3_IMAGES_BUCKET=<images bucket>
S3_CSV_BUCKET=<csv bucket>
S3_BUCKET=<images bucket>
```

`S3_BUCKET` is the images bucket. Lesson 06 uploads into it. The container reads `S3_BUCKET` and writes to `S3_CSV_BUCKET`.
