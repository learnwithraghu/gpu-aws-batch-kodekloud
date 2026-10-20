# Lesson 00 — The real job

KodeFood is a fast-food delivery app. Millions of users. More than 2,000 vendors, and more joining every day. One hard problem is the photo a vendor uploads. Someone still checks it by hand.

**Demo / Lab (Section 001):** [Demo] Current manual menu image verification — run the vendor portal below to feel that manual queue before the course replaces it with AWS Batch.

This course then builds the simple design: run a finished caption model on each photo. A food-like caption accepts the photo and becomes the menu text. A caption about a car, a selfie, or a logo rejects the photo. Nobody on the team has to open every upload.

Theory reading: [`theory.md`](theory.md). Portal how-to: [`vendor_portal/README.md`](vendor_portal/README.md).

## Demo 007 — Current manual menu image verification

Show the **legacy** vendor experience: upload menu photos, submit, get a 24-hour human-review promise. No GPU. No Batch.

### Local dry run

```bash
cd lessons/00-the-real-job/vendor_portal
bash run_portal.sh
# open http://127.0.0.1:8000
```

### EC2 (Amazon Linux 2023) — instructor / Lab 008 path

1. Launch a `t3.micro` with inbound **SSH 22** and **TCP 8000** from your IP.
2. Clone the course repo on the instance, then:

```bash
cd gpu-aws-batch-kodekloud/lessons/00-the-real-job/vendor_portal
bash setup_ec2.sh
# MODE defaults to manual
```

3. Open `http://<public-ip>:8000`.
4. Upload several dish photos (optionally add a selfie or logo). Confirm **Pending Manual Review**.
5. Click **Submit Menu Photos**. Confirm the banner:
   > Submitted! One of your account managers will review this in 24 hours and get back to you.

Later in the course (Section 007 Demo 005), the same app runs with `MODE=batch` and shows accept/reject decisions from `descriptions.csv`.

## What arrives (after Batch exists)

```
s3://<images-bucket>/images/<batch>/
```

`<batch>` is the folder name. The commands in this course use `sample`. Only `.jpg`, `.jpeg`, and `.png` are described.

## What the GPU produces

One job, one file:

```
s3://<descriptions-bucket>/descriptions/<batch>/descriptions.csv
```

```csv
image_s3_uri,item_description,photo_status
s3://<images-bucket>/images/sample/bowl.jpg,a food dish of noodles with vegetables,accepted
s3://<images-bucket>/images/sample/car.jpg,a car parked on the street,rejected
```

Rejected rows stay in the file so the reason is visible. The app uses the accepted rows for the menu.

The model sees 8 photos at a time so they fit in GPU memory. Those groups are not extra files. The app reads this CSV, not the image folder.

## Why a GPU, and why it is a batch job

Checking a folder is the same model run over many images. A CPU can do it. A GPU finishes the folder in one short run. KodeFood does not keep a GPU switched on per vendor. A shared pool starts when folders are waiting and can go back to zero when the queue is empty. That is the job this course puts on AWS Batch.
