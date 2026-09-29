# Video 08 — Idempotent CSV output
**Type:** Theory
**Runtime target:** ~3 minutes

---

Okay, so the CSV path is part of the product contract.

The output key is derived from the input prefix, so the same folder always means the same object. In photos.py, save_csv takes the last segment of PREFIX. images/sample becomes sample. The key is descriptions/sample/descriptions.csv, in the CSV bucket. A second successful run for that same prefix calls put_object on that same key. S3 replaces the object. The latest successful run wins. The catalog for that stem is whatever the last good job wrote.

That choice keeps operations and the app pointed at one path per vendor. You don't accumulate catalog_v3_final.csv, then a copy with a date in the name. images/vendor-b always lands at descriptions/vendor-b/descriptions.csv. Anyone who knows the prefix knows the CSV URI without listing the bucket to find the newest name.

The write is also late on purpose. describe_items.py builds the full list of rows in memory, group by group, each with image_s3_uri, item_description, and photo_status, and calls photos.save_csv only after the loop finishes. A failed run shouldn't publish a half-written contract. If the folder is empty, main raises SystemExit with No images to describe before save_csv runs, so an empty submit doesn't wipe a previous good file. If a later group throws during download or generate, put_object hasn't been called yet, and the previous object stays as it was. Rejected rows stay in that file so the reason is visible. The app uses the accepted rows for the menu.

Picture a fix to the prompt. You change a photography of, or you change num_beams, in describe_items.py. You rebuild the image and you push it, because Batch runs the registry copy, then you resubmit the same IMAGE_PREFIX. The new sentences replace the old sentences at the same URI. The app doesn't need a new path. A run that dies in the middle leaves that URI alone, still holding the previous success.

The key is built in one place, inside save_csv. The buffer gets the header image_s3_uri, item_description, and photo_status, then every triple the loop appended. csv.writer quotes a description that contains a comma. put_object sends the whole buffer in one call to CSV_BUCKET. The print reports how many rows were written, how many were accepted, how many were rejected, and the s3 URI. If that line never shows up, the object at that key wasn't replaced.

Lesson three packages this program into an image. Next you'll see why a GPU job needs that container, and why the container still depends on the NVIDIA drivers on the host.
