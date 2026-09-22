# Step 04 — Submit and wait

Submit the whole-batch job from step 03 and poll until it finishes.
Same submit + poll pattern as lesson 02 — now with environment variables
that tell the container what to process.

**Run:** `python main.py [--batch-stem sample]`

**Expected:** `✅ Job SUCCEEDED` and the S3 path of the caption file.
