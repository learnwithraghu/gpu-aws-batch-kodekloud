# Step 03 — Check results

One S3 listing + one CSV read per batch: every caption folder in the bucket,
with the number of captions in each.

**Run:** `python main.py`

**Expected:**

```
Caption files in s3://<bucket>/captions/:

          sample :   12 captions
       batch01   :   12 captions
       batch02   :   12 captions

          TOTAL :   36 captions
```
