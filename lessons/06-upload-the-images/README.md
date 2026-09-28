# Lesson 06 — Upload the images

Put one vendor folder where the container will look: `images/<batch>/` in the images bucket from lesson 05.

Theory reading: [`theory.md`](theory.md).

```bash
set -a && source .env && set +a
```

## Sync

From a local folder of photos:

```bash
aws s3 sync ./photos "s3://${S3_BUCKET}/images/sample/" \
  --exclude "*" --include "*.jpg" --include "*.jpeg" --include "*.png"
```

Change `sample` if this batch uses another folder name. About 25–30 photos is a normal vendor drop. You do not rebuild the image for new photos. The job reads S3 when it runs.

## Check

```bash
aws s3 ls "s3://${S3_BUCKET}/images/sample/"
```

Every photo for this batch should be listed. That list is what one job turns into one CSV.

If files were uploaded to the bucket root instead of `images/sample/`, move them before you submit:

```bash
bash helpers/organize_uploads.sh --stem sample
```

`--dry-run` prints the moves and copies nothing.
