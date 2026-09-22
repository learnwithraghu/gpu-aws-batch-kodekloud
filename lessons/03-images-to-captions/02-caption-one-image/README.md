# Step 02 — Caption ONE image

Before scaling to a batch, caption a single image. `job.py` (runs on the GPU
in Batch) downloads one image from S3, loads BLIP, prints one caption.
`main.py` submits it and polls.

**Run:** `python main.py [--image <filename>]`

**Expected:** the CloudWatch log stream shows:

```
Device  : cuda
Image   : s3://<bucket>/images/sample/dog.jpg
Caption : a dog running across a grassy park
```
