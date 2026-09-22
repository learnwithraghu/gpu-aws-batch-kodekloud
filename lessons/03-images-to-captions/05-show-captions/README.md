# Step 05 — Show captions

Download the caption file from S3 and print it: one numbered line per image,
caption first, S3 URI underneath.

**Run:** `python main.py [--batch-stem sample]`

**Expected:**

```
12 captions in s3://<bucket>/captions/sample/captions.csv

  1. a dog running across a grassy park
      s3://<bucket>/images/sample/dog.jpg
  ...
```
