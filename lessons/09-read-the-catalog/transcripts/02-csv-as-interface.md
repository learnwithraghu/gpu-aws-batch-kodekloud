# Video 02 — CSV as interface
**Type:** Theory
**Runtime target:** ~3 minutes

---

Okay, so those column names matter more than they look. The catalog file has three columns, and those names are an API. The header is image_s3_uri, item_description, photo_status. image_s3_uri is the full S3 URI of one photo. item_description is the sentence the model wrote. photo_status is accepted when the caption looks like food, and rejected when it does not. Rejected rows stay in the file so the reason is visible. KodeFood uses the accepted rows for the menu. Rename a column without updating the app and the consumer breaks.

The contract is stable on purpose. Adding a column carefully can be fine if old readers still find the three names. Silently changing what item_description or photo_status means is not fine. Treat this file like a small schema between the model and the product. The app never asks Batch what the schema is. It reads the object.

The course key is descriptions, stem, descriptions.csv in the CSV bucket. IMAGE_PREFIX images/sample becomes descriptions/sample/descriptions.csv. One row looks like this. Image URI points at images/sample/bowl.jpg. Description says a food dish of noodles with vegetables. Status is accepted. A car photo can say a car parked on the street and mark rejected. A description with a comma is quoted by the CSV writer, so the three columns still split cleanly. A second successful run for the same stem overwrites this key. Readers always open one path. They do not look up a job id.

That row exists because the job wrote it. Command python /app/describe_items.py. Environment had the buckets, IMAGE_PREFIX, and BATCH_SIZE. BATCH_SIZE eight groups GPU work. It does not split the catalog into eight CSVs. The program lists jpg, jpeg, and png, captions them, marks each accepted or rejected, and writes one file after every photo succeeds. Job definition gpu-teaching-caption-job, highest active revision, one GPU, twelve thousand two hundred eighty-eight mebibytes, queue gpu-teaching-gpu-smoke-queue-spot in ap-northeast-1. SUCCEEDED means exit zero. The interface the app trusts is still these three column names on this key.

If a later program printed a friendlier header or swapped column order, every reader would fail while Batch stayed green. The fix is a consumer migration, not a quieter job status.

The next check is the row count against the photos the job was allowed to see.
