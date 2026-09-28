# Lesson 06 — Theory

This lesson moves photos into the prefix the container will list. No Docker rebuild.

## `sync` vs `cp`

`aws s3 cp` copies one object (or a recursive tree with the right flags). `aws s3 sync` mirrors a local directory to a prefix: upload new and changed files, skip ones that already match.

For a vendor drop of ~25–30 photos, `sync` with includes for `.jpg` / `.jpeg` / `.png` is the natural tool. Re-running sync after adding three photos only uploads what changed.

## Prefix contracts

The job reads `IMAGE_PREFIX` (for example `images/sample`). Only keys under that prefix are candidates for the CSV.

Photos at the bucket root, or under `images/other/`, are invisible to a job aimed at `images/sample/`. The upload path and the submit override must agree. Lesson 08 sets `IMAGE_PREFIX` to match what you sync here.

## File types and silent skips

`photos.py` keeps keys ending in `.jpg`, `.jpeg`, or `.png` (case-insensitive). A `.gif`, `.heic`, or README in the folder is skipped — no row, no error for that file.

If students expect 30 rows and get 28, check for non-supported extensions before blaming the GPU. The contract is intentional: the catalog is for common photo types vendors actually send.

## Data size vs image size

A few megabytes on S3 is not the same as GPU memory use. The job downloads bytes, decodes them into RGB tensors, and runs the model. Decoded batches of 8 use far more device memory than the JPEG sizes suggest.

That is why lesson 02 micro-batches by count (8 photos), not by “total MB on S3.” Large files can also slow download and CPU decode before the GPU starts.

## Don’t rebuild for new photos

New vendor photos are **data**. They live in S3. The container image is **code and dependencies**.

Upload more photos → sync only (this lesson). Change `describe_items.py` or the Dockerfile → rebuild and push (lessons 03–04), then submit again. Mixing those two up wastes time: either you rebuild for nothing, or you submit and wonder why old caption logic still runs.
