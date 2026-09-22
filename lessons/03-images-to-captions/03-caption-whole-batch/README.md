# Step 03 — Caption the whole batch

This is the real container job: download every image under the prefix,
run BLIP over them in GPU batches of 8, and write one caption file to S3 —

```
s3://<bucket>/captions/<stem>/captions.csv   (columns: image_s3_uri, caption)
```

**Run:** nothing to execute here — step 04 submits this script.

**Expected (when run):** progress lines per batch of 8, ending with
`Uploaded caption file to s3://<bucket>/captions/<stem>/captions.csv`.
