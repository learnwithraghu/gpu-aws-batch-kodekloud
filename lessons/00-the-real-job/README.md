# Lesson 00 — The real job

KodeFood is a fast-food delivery app. Millions of users. More than 2,000 vendors, and more joining every day. One hard problem is the photo a vendor uploads. Someone still checks it by hand.

This course builds the simple design: run a finished caption model on each photo. A food-like caption accepts the photo and becomes the menu text. A caption about a car, a selfie, or a logo rejects the photo. Nobody on the team has to open every upload.

Theory reading: [`theory.md`](theory.md).

No AWS commands in this lesson. Later lessons build the pieces that make this run.

## What arrives

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
