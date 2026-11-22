# Restaurant portal (S3 upload)

This is the same KodeFood back office from [01 — Restaurant portal](../../01-restaurant-portal/), wired with `boto3` so every added dish photo is uploaded immediately to `s3://kodefood-menu-uploads-kodekloud/uploads/` in **Tokyo (`ap-northeast-1`)**.

Complete [03a — Create the S3 bucket](../03a-create-s3-bucket/GUIDE.md) first, and confirm your local AWS credentials are configured (`aws configure`).

## What changed from 01

- `requirements.txt` adds `boto3` (`boto3==1.37.18`).
- `app.py` uploads each dish photo to S3 when you click **Add to this update**, deletes the S3 object if you click **Remove** before submitting, and leaves S3 objects intact when you click **Start another update**.
- `templates/index.html` and `static/style.css` are untouched copies from `01-restaurant-portal`.

## Run locally with Python

```bash
cd 03-s3-upload/03b-restaurant-portal-s3
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

If you chose a custom bucket name in `03a`:

```bash
S3_BUCKET=your-bucket-name python app.py
```

If `01-restaurant-portal` is still running on port `8000`:

```bash
PORT=8001 python app.py
```

## Or run in Docker

From the **repo root**:

```bash
docker build -f 03-s3-upload/03b-restaurant-portal-s3/Dockerfile -t kodefood-restaurant-portal-s3:latest .
```

Run the container, exporting your local AWS CLI credentials at runtime (so no keys are baked into the image):

```bash
eval "$(aws configure export-credentials --format env)"
docker run --rm --name kodefood-restaurant-portal-s3 \
  -p 8000:8000 \
  -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e AWS_SESSION_TOKEN \
  -e AWS_DEFAULT_REGION=ap-northeast-1 \
  -e S3_BUCKET=kodefood-menu-uploads-kodekloud \
  kodefood-restaurant-portal-s3:latest
```

Stop and clean up the container and image:

```bash
docker rm -f kodefood-restaurant-portal-s3 2>/dev/null || true
docker rmi -f kodefood-restaurant-portal-s3:latest 2>/dev/null || true
```

## What to click and verify in S3

1. Open http://127.0.0.1:8000.
2. Pick a sample photo, or upload your own.
3. Write the name of that photo and choose **Add to this update**. Confirm the banner displays `Uploaded to s3://kodefood-menu-uploads-kodekloud/uploads/...`.
4. Repeat for any additional dishes, then choose **Update our menu**.
5. Open **Amazon S3** → **`kodefood-menu-uploads-kodekloud`** → **`uploads/`** in the AWS Console (or run `aws s3 ls s3://kodefood-menu-uploads-kodekloud/uploads/ --region ap-northeast-1`) to verify the uploaded photos are stored in S3.
6. **Start another update** clears the local desk while keeping the uploaded photos in S3, ready for step 04 (AWS Batch GPU-powered ML scoring).
