# Lesson 03 — Images → Captions

> **Concepts**: Image captioning · BLIP · S3 I/O from a Batch job
> **AWS needed**: Batch, S3

---

## What Is Image Captioning?

Image captioning means generating a natural-language sentence that describes
what's in a photo — e.g. `"a dog playing in a park"`. It's the bridge between
raw pixels and searchable text.

We process a **folder of standalone images** in this lesson (not video frames)
— exactly the kind of dataset you'd have from a photo library, a product
catalog, or a set of scanned documents.

---

## Why Run Captioning on GPU?

Image captioning uses a neural network (BLIP) with a vision encoder + text
decoder. Running it one image at a time on CPU takes ~1–2 seconds; on GPU it
takes well under 100 ms. For a batch of images, that difference compounds
fast — this is a textbook GPU batch-inference workload.

**Main lesson**: How to read from S3, do work, write back to S3 — the
standard Batch I/O pattern.

---

## What Is BLIP?

BLIP (Bootstrapping Language-Image Pretraining) is a vision-language model
that can look at an image and generate a caption for it. We use the small
`Salesforce/blip-image-captioning-base` checkpoint (~1 GB), which fits
comfortably in the T4's 16 GB VRAM.

---

## The S3 Pattern

Every Batch job in this course follows the same I/O pattern:

```
S3 (input)  →  download to /tmp  →  process  →  upload results to S3  →  done
```

The job reads `S3_BUCKET` and `IMAGE_PREFIX` from environment variables
(passed at submit time), and writes one caption file per image batch to
`captions/<batch-stem>/captions.csv`:

```csv
image_s3_uri,caption
s3://your-bucket/images/sample/dog.jpg,"a dog running across a grassy park"
```

Each row pairs the **S3 location of the image** with **the caption BLIP
generated for it** — a simple, portable record of the whole batch that any
downstream tool (pandas, a spreadsheet, another job) can read.

---

## The Steps

Six short demos — cd in, run `python main.py`:

| Step | You learn | Time |
|------|-----------|------|
| [00-register-job-def](00-register-job-def/) | Point Batch at the ECR image (job definition) | 5 min |
| [01-upload-images](01-upload-images/) | Push sample images to S3 | 5 min |
| [02-caption-one-image](02-caption-one-image/) | BLIP captions ONE image on the GPU | 10 min |
| [03-caption-whole-batch](03-caption-whole-batch/) | The real container job → captions.csv | 10 min |
| [04-submit-and-wait](04-submit-and-wait/) | Submit + poll the batch job | 15 min |
| [05-show-captions](05-show-captions/) | Print the caption table | 2 min |

---

## Key Takeaway

> The S3 ↔ Batch I/O pattern is the backbone of every lesson. Learn it here
> and the rest flows naturally.
