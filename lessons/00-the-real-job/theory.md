# Lesson 00 — Theory

Short reading before the rest of the course. No AWS commands here.

## Batch inference vs training

Training updates model weights from labeled data. Inference runs a finished model on new inputs and produces answers.

This course is inference only. A vendor folder of dish photos goes in. A short catalog sentence per photo comes out. You do not fine-tune BLIP, and you do not need a training loop, optimizer, or labeled dataset. The GPU’s job is to run the same forward pass many times, once per photo (in small groups).

## Why GPUs help image models

An image is a large grid of numbers. Caption models turn those numbers into text with a lot of matrix math. A CPU can do that math one (or a few) operations at a time. A GPU runs many of those operations together.

For a folder of about 25–30 photos, both can finish eventually. The GPU finishes the folder in one short run. That is why this course asks AWS Batch for a GPU instance instead of a small CPU box.

## Always-on GPU vs on-demand batch

A `g4dn.xlarge` left running all day costs money even when no vendor uploads anything. Food catalogs often arrive as rare drops: hours or days apart.

A batch design starts a GPU only when a folder is waiting, then lets capacity go back to zero. You pay for the minutes the job needs, not for idle time between drops. That is the shape of AWS Batch with `minvCpus` set to 0.

## One folder, one artifact

Good batch jobs have a clear contract: one input location, one output object.

In this course the contract is:

- Input: `images/<batch>/` in the images bucket
- Output: `descriptions/<batch>/descriptions.csv` in the CSV bucket

Groups of 8 inside the GPU are only how many photos fit in memory at once. They are not eight separate catalog files. The food app reads one CSV per vendor folder.

## Catalog text as a product

The food app does not open the image folder to invent titles. It reads rows:

```csv
image_s3_uri,item_description
```

Each row ties a photo URI to a short description. That file is the product. If the CSV is wrong, the app is wrong — even if the GPU “ran fine.” Later lessons judge success by that object existing and having one row per photo.

## Where AWS fits later

Three AWS pieces appear after this lesson:

| Piece | Holds | Later lesson |
|-------|--------|--------------|
| S3 | Photos and the catalog CSV | 05, 06, 09 |
| ECR | The Docker image with CUDA, PyTorch, and your code | 03, 04 |
| AWS Batch | Schedules a GPU machine to run that image | 01, 07, 08 |

S3 is data. ECR is the program and its dependencies. Batch is the scheduler that turns those two into a finished CSV without leaving a GPU on overnight.
