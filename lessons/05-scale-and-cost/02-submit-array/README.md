# Step 02 — Submit an array job

One submission → N parallel containers. Each element gets
`AWS_BATCH_JOB_ARRAY_INDEX` (0, 1, 2, …), looks up its image prefix in a JSON
list stored in S3, and runs `generate_captions.py` on that batch.

**Run:**

```bash
# Upload extra image batches first (folders of .jpg/.png), e.g.:
aws s3 cp my-images/ s3://<bucket>/images/batch01/ --recursive

# One array element per image prefix:
python main.py --image-prefixes images/batch01 images/batch02 images/batch03
```

**Expected:** `statusSummary` shows elements finishing in parallel, ending
with `✅ Array job SUCCEEDED`. Each batch gets its own `captions/<stem>/captions.csv`.
