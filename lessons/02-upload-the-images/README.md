# Lesson 02 — Upload the images

Put one vendor folder where the job will look: `images/<batch>/` in the images bucket.

## Target prefix

```
s3://<images-bucket>/images/<batch>/
```

Only `.jpg`, `.jpeg`, and `.png` are described. Other files in the folder are skipped.

## The command

From a local folder of photos, with `S3_BUCKET` set from `.env`:

```bash
aws s3 sync ./photos "s3://${S3_BUCKET}/images/sample/" \
  --exclude "*" --include "*.jpg" --include "*.jpeg" --include "*.png"
```

Change `sample` if this batch uses another stem. About 25–30 photos is a normal vendor drop.

## Root-level leftovers

If photos were uploaded to the bucket root instead of `images/<batch>/`, move them:

```bash
bash helpers/organize_uploads.sh --stem sample
```

`--dry-run` prints the moves and does not copy anything.

## Check

```bash
aws s3 ls "s3://${S3_BUCKET}/images/sample/"
```

Every photo for this batch should be listed. That list is what one job run will turn into one CSV.
