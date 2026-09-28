# Lesson 00 — The real job

A food vendor drops one folder of dish photos, about 25–30 pictures. A GPU writes one catalog line per photo. The food app reads that file. The GPU machine does not stay on between drops.

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
image_s3_uri,item_description
s3://<images-bucket>/images/sample/bowl.jpg,a food dish of noodles with vegetables
```

The model sees 8 photos at a time so they fit in GPU memory. Those groups are not extra files. The app reads this CSV, not the image folder.

## Why a GPU, and why it is a batch job

Describing a folder is the same model run over many images. A CPU can do it. A GPU finishes the folder in one short run. The next vendor folder might be hours away, so the machine should exist only while a folder is waiting. That is the job this course puts on AWS Batch.
