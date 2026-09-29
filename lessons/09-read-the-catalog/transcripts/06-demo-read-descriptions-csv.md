# Video 06 — Demo: read the catalog CSV
**Type:** Demo
**Runtime target:** ~3 minutes

---

Alright. Last demo. Let's open the CSV. I want to prove the artifact, not just the Batch status. The job from the previous lesson has to be SUCCEEDED. A green status on a different stem does not count. KodeFood will read this object and nothing else.

I am in the terminal. I load the env file with set -a, source .env, set +a, so S3_CSV_BUCKET is set.

I run aws s3 cp. Source is s3, S3_CSV_BUCKET, descriptions/sample/descriptions.csv. Destination is a dash so it prints in the terminal. If I had submitted a different stem, I would change sample in that key. The submit prefix was images/sample, and the program turns that stem into this key.

A healthy print starts with header image_s3_uri, item_description, photo_status. Then one row per photo. Each image URI points under images/sample and ends in jpg, jpeg, or png. One course example is bowl.jpg with a food dish of noodles with vegetables, photo_status accepted. A car photo can say a car parked on the street and mark rejected. Rejected rows stay in the file. The app uses the accepted rows for the menu. BATCH_SIZE eight did not create eight files. There is one CSV.

I run the same aws s3 cp again and pipe to wc -l. Subtract one for the header. That is how many photos the GPU described, accepted and rejected together. I compare it to jpg, jpeg, and png keys under images/sample, not every object in the folder. A heic will not have a row. Fewer rows than supported keys means a skipped extension or the wrong stem. More rows means extra photos were already in the prefix. This program writes the CSV only after all selected photos succeed, so a short file is not a partial crash dump.

If I want a local copy, I run aws s3 cp a third time to ./descriptions.csv. Optional. The object in the CSV bucket is what the app reads.

I do not call describe-jobs to validate the schema. SUCCEEDED already said exit zero. Columns and count are an S3 fact. Logs in /aws/batch/job would show each photo as key, arrow, caption, and accepted or rejected in brackets, plus a Wrote line with accepted and rejected counts from photos.save_csv. Those lines exist only after STARTING or RUNNING. They are the worker's log. They are not the menu.

The GPU can scale away when the queue goes idle. The CSV stays. That file, with those three columns, is what KodeFood ships against. That is the end of the course.
