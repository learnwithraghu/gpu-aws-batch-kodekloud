# 03a — Create the S3 bucket

In [01 — Restaurant portal](../../01-restaurant-portal/), uploaded dish photos only stayed on local disk. Now we create a private S3 bucket in Tokyo so the portal can store each uploaded dish photo in the cloud, ready for a later AWS Batch GPU job (step 04) to pick it up for ML-powered scoring.

## Open the console

1. Sign in to the AWS console.
2. In the top bar, set the region to **Asia Pacific (Tokyo) `ap-northeast-1`**.
3. Open **Amazon S3** → **General purpose buckets** (or **Buckets**) → **Create bucket**.

## Configure the bucket

1. **AWS Region**: confirm **Asia Pacific (Tokyo) `ap-northeast-1`** (the same region as the Batch compute environments in `02-aws-batch`).
2. **Bucket type**: **General purpose**.
3. **Bucket name**: **`kodefood-menu-uploads-kodekloud`**
   - S3 bucket names are globally unique across all AWS accounts. If this exact name is already taken, append a short suffix (for example `kodefood-menu-uploads-kodekloud-123`) and pass `S3_BUCKET=<your-bucket-name>` when running step `03b`.
4. **Object Ownership**: leave **ACLs disabled (recommended)**.
5. **Block Public Access settings for this bucket**: keep **Block *all* public access** checked. Dish photos stay private; AWS Batch will access them through IAM in step 04 rather than public URLs.
6. **Bucket Versioning**: leave **Disable**.
7. **Tags**: leave empty.
8. **Default encryption**: leave **Server-side encryption with Amazon S3 managed keys (SSE-S3)** and **Bucket Key** set to **Enable**.
9. **Advanced settings**: leave **Object Lock** disabled.
10. Choose **Create bucket**.

## Verify the bucket and local CLI access

1. Confirm **`kodefood-menu-uploads-kodekloud`** appears in **General purpose buckets** with region **Asia Pacific (Tokyo) `ap-northeast-1`**.
2. Optional local terminal check (verifies your `aws configure` credentials can reach the bucket before starting `03b`):
   ```bash
   aws s3 ls s3://kodefood-menu-uploads-kodekloud --region ap-northeast-1
   ```
   An empty output with exit code `0` means the bucket exists and your local credentials have access.

## Leave these alone

- Do not modify or delete `gpu-teaching-images-*` or `gpu-teaching-captions-csv-*`.
- Keep `kodefood-menu-uploads-kodekloud` for step 04 (do not delete it yet).

## You are done when

`kodefood-menu-uploads-kodekloud` exists in `ap-northeast-1` with **Block all public access** enabled and your local AWS CLI can list it.

Next: [03b — Run the restaurant portal with S3 upload](../03b-restaurant-portal-s3/README.md).
