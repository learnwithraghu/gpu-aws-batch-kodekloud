# 03 — Upload portal photos to S3

Connect the restaurant portal from [01 — Restaurant portal](../01-restaurant-portal/) to Amazon S3 in **Asia Pacific (Tokyo) `ap-northeast-1`**. Every dish photo added in the portal is stored in S3 so a later AWS Batch GPU job (step 04) can pick it up for ML-powered scoring.

This walkthrough uses a separate `kodefood-*` bucket and leaves the existing `gpu-teaching-*` resources alone.

| Step | What you do | Done when |
|------|-------------|-----------|
| [03a](03a-create-s3-bucket/GUIDE.md) | Create S3 bucket `kodefood-menu-uploads-kodekloud` | Bucket exists in `ap-northeast-1` with Block all public access enabled. |
| [03b](03b-restaurant-portal-s3/README.md) | Run the restaurant portal wired to S3 | Local portal uploads a dish photo and the file appears under `uploads/` in S3. |

Open [step 03a](03a-create-s3-bucket/GUIDE.md).
