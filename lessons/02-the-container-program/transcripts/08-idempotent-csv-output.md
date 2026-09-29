# Video 08 — Idempotent CSV output
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

The output key is derived from the input prefix, so the same folder always means the same object. In photos.py, save_csv takes the last segment of PREFIX. images/sample becomes sample. The key is descriptions, slash, that folder name, slash, descriptions.csv. For the sample folder that's descriptions/sample/descriptions.csv, in the CSV bucket. A second successful run for that same prefix calls put_object on that same key. S3 replaces the object. The latest successful run wins. The catalog for that stem is whatever the last good job wrote.

That choice keeps operations and the app pointed at one path per vendor. You don't accumulate catalog_v3_final.csv, then a copy, then another copy with a date in the name. images/vendor-b always lands at descriptions/vendor-b/descriptions.csv. The stem is the last path segment, so the descriptions folder mirrors the vendor folder you submitted. Anyone who knows the prefix knows the CSV URI without listing the bucket to find the newest name.

The write is also late on purpose. describe_items.py builds the full list of rows in memory, group by group, and calls photos.save_csv only after the loop finishes. A failed run shouldn't publish a half-written contract. If the folder is empty, main raises SystemExit with No images to describe before save_csv runs, so an empty submit doesn't wipe a previous good file with a header and zero rows. If a later group throws during download or generate, put_object hasn't been called yet, and the previous object stays as it was. The groups aren't partial CSVs. They're rows that only become a file at the end.

Picture a fix to the prompt. You change a photography of, or you change num_beams, in describe_items.py. You rebuild the image and you push it, because Batch runs the registry copy, then you resubmit the same IMAGE_PREFIX. The new sentences replace the old sentences at the same URI. The app doesn't need a new path. It reads descriptions/sample/descriptions.csv and sees the latest success. A run that dies in the middle leaves that URI alone, still holding the previous success.

The key is built in one place, inside save_csv, so the GPU loop can't invent a second filename. folder is the last segment of PREFIX after the split. out_key is descriptions, then that folder, then descriptions.csv. The buffer gets the header image_s3_uri and item_description, then every pair the loop appended. csv.writer quotes a description that contains a comma, so a caption with a comma stays one record. put_object sends the whole buffer in one call to CSV_BUCKET. The print after that's the line you look for. It reports how many descriptions were written and the s3 URI. If that line never shows up, the object at that key wasn't replaced.

On the screen, draw two submit arrows, both labeled images/sample, both pointing at one S3 key, descriptions/sample/descriptions.csv. The second arrow replaces the body of that object. A third arrow, a job that fails halfway, stops before the key and leaves the body untouched.

Lesson three packages this program into an image. Next you'll see why a GPU job needs that container, and why the container still depends on the NVIDIA drivers on the host.
