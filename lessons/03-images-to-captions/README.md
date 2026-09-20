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
(passed at submit time), and writes a caption manifest to
`captions/<batch-stem>/manifest.json`.

---

## What the Notebook Does

1. Uploads the images in `assets/images/` (committed in this folder) to S3
2. Submits the captioning job to Batch
3. After the job completes, downloads the caption manifest and displays a few
   images next to their generated captions

---

## Key Takeaway

> The S3 ↔ Batch I/O pattern is the backbone of every lesson. Learn it here
> and the rest flows naturally.
