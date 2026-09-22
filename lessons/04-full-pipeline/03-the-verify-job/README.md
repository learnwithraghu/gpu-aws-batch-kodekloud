# Step 03 — The verify job

`verify_captions.py` is the container script that Job 2 runs. Nothing to
execute here — read it to see what verification does:

1. Counts the images under the image prefix in S3
2. Downloads `captions/<stem>/captions.csv` from Job 1
3. Checks every image has exactly one caption — exits non-zero on mismatch,
   which fails the Batch job
4. Writes a `_VERIFIED` marker to S3 as proof the pipeline completed

**Run:** nothing — step 02 submits it.
