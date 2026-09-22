# Step 01 — Upload images

Push the sample images from `assets/images/` (lesson root) to S3. Everything
else in this lesson reads from there.

**Run:** `python main.py [--batch-stem sample]`

**Expected:** one `Uploading …` line per image, ending with
`Uploaded N images to s3://<bucket>/images/sample/`.

Place 5–20 `.jpg`/`.png` photos in `assets/images/` first — see
[assets/README.md](../assets/README.md).
