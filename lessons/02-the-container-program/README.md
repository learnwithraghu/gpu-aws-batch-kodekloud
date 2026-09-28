# Lesson 02 — The container program

[`describe_items.py`](describe_items.py) is the program the GPU runs. It does not create buckets, registries, or Batch resources. Those are the later lessons. This file only lists a folder, describes the photos, and writes one CSV.

It runs inside the image, at `/app/describe_items.py`. Running it on your laptop does nothing useful unless that laptop has the same GPU stack and the same environment variables.

## What the job receives

Batch injects these when you submit. They are not hard-coded.

| Variable | Meaning |
|----------|---------|
| `S3_BUCKET` | Images bucket |
| `S3_CSV_BUCKET` | Bucket that receives the CSV |
| `IMAGE_PREFIX` | Folder to read, such as `images/sample` |
| `BATCH_SIZE` | Photos per GPU pass. Default 8 |

The container uses the job role from lesson 01 for these S3 calls.

## What it does

1. Load BLIP (`Salesforce/blip-image-captioning-base`) onto `cuda` when CUDA is visible.
2. List `IMAGE_PREFIX/` and keep `.jpg`, `.jpeg`, and `.png`.
3. Prompt each photo with `a food dish of`, 8 photos at a time.
4. Write one object: `descriptions/<folder>/descriptions.csv` with columns `image_s3_uri` and `item_description`.

`<folder>` is the last part of `IMAGE_PREFIX`. `images/sample` becomes `sample`.

An empty list exits the job. The groups of 8 never become separate files.

## Where this file goes next

Lesson 03 copies this file into a local image. Lesson 04 pushes that image. Lesson 08 tells Batch to run `python /app/describe_items.py`. A change to this file is invisible to Batch until you build and push again.
