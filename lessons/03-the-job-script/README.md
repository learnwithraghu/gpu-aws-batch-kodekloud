# Lesson 03 — The job script

Read [`describe_items.py`](describe_items.py) in this folder. It runs inside the GPU container, not on your laptop. Do not submit a job in this lesson.

## Inputs

The container reads:

| Variable | Meaning |
|----------|---------|
| `S3_BUCKET` | Images bucket |
| `S3_CSV_BUCKET` | Bucket that receives the CSV. Defaults to `S3_BUCKET` |
| `IMAGE_PREFIX` | Folder to read, such as `images/sample` |
| `BATCH_SIZE` | Photos per GPU pass. Default 8 |

Lesson 06 `submit_job.py` sets these when you submit. They are not hard-coded in the script.

## Listing

The script lists every object under `IMAGE_PREFIX/` and keeps keys that end in `.jpg`, `.jpeg`, or `.png`. The list is sorted, then described from top to bottom. An empty list stops the job.

## Describing

BLIP (`Salesforce/blip-image-captioning-base`) runs on the GPU. Each photo is prompted with `a food dish of`. The model sees 8 photos at a time so a 25–30 photo folder stays within GPU memory.

## Output

After every photo has a description, the script writes one object:

```
s3://<csv-bucket>/descriptions/<folder>/descriptions.csv
```

`<folder>` is the last part of `IMAGE_PREFIX` (`images/sample` becomes `sample`). Columns are `image_s3_uri` and `item_description`.

The groups of 8 never become separate files. One folder in, one CSV out.
