# Video 02 — CSV as interface
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

The catalog file has two columns, and those names are an API. The header is image_s3_uri, then item_description. image_s3_uri is the full S3 URI of one photo. item_description is the sentence the model wrote for that photo. The food app maps those columns onto fields. Rename a column without updating the app and the consumer breaks, the same way a renamed JSON field breaks a public REST API.

The contract is stable on purpose. Adding a column carefully can be fine, if old readers still find the two names they already use. Silently changing what item_description means is not fine. A prompt change that makes every sentence longer, or that stops describing the food, is a behavior change in a public field. Treat this file like a small schema between the model and the product. The app never asks Batch what the schema is. It reads the object.

The course key is descriptions, then the folder stem, then descriptions.csv, in the CSV bucket. IMAGE_PREFIX images/sample becomes descriptions/sample/descriptions.csv. One row in that file looks like this. The image URI is s3, then the images bucket, then images/sample/bowl.jpg. The description is a food dish of noodles with vegetables. The bucket in that URI is the name S3_BUCKET had on the submit. The path under it is the photo key. The sentence is the shape of item_description, one caption, not a second file. A description that contains a comma is quoted by the CSV writer, so the two columns still split in the same place. A second successful run for the same stem overwrites this key. Readers always open one path. They do not look up a job id to find the file. A rename of item_description is a breaking change for those readers. A careful extra column is something an old reader can ignore.

That row only exists because the job wrote it. The command was python /app/describe_items.py. The environment had S3_BUCKET, S3_CSV_BUCKET, IMAGE_PREFIX, and BATCH_SIZE. BATCH_SIZE eight groups the GPU work. It does not split the catalog into eight CSVs. The program lists jpg, jpeg, and png keys, captions them, and writes this one file after every photo in the group list succeeds. The job definition name is gpu-teaching-caption-job, highest active revision, one GPU, twelve thousand two hundred eighty-eight mebibytes, queue gpu-teaching-gpu-smoke-queue-spot in ap-northeast-1. SUCCEEDED means that process exited zero. The interface the app trusts is still these two column names on this key.

If a later revision of the program printed a friendlier header, or swapped the column order, every reader built on this lesson would fail while Batch stayed green. The fix is a migration of the consumer, not a quieter job status.

On the screen, the CSV sits as a tiny schema document between the model and the product, with those two column names large enough to read, and one sample row underneath.

The next check is the row count, against the photos the job was allowed to see.
