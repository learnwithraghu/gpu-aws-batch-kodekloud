# Video 06 — Demo: read the catalog CSV
**Type:** Demo
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

I want to prove the artifact, the way product and engineering would, not just the Batch status. The job from the previous lesson has to be SUCCEEDED before this file is the catalog. A green status on a different stem does not count. The app will read this object and nothing else.

I am in the terminal. I load the env file with set -a, then source .env, then set +a, so S3_CSV_BUCKET is the CSV bucket name. The bucket name comes from that variable.

I run aws s3 cp. The source is s3, then S3_CSV_BUCKET, then descriptions/sample/descriptions.csv. The destination is a single dash, so the file prints in the terminal instead of landing on disk. If I had submitted a different folder stem, I would change sample in that key to match. The prefix on the submit was images/sample, and the program turns that stem into this key.

A healthy print starts with the header image_s3_uri, item_description. Then one row per photo the job described. Each image URI points at the images bucket, under images/sample, and ends in jpg, jpeg, or png. One row in the course example is the bowl photo, images/sample/bowl.jpg, with a description such as a food dish of noodles with vegetables. The sentences are readable captions, not empty fields, and not a second header. BATCH_SIZE eight did not create eight files. There is one CSV.

I run the same aws s3 cp again, same source, same dash, and I pipe it to wc -l. The number that comes back is the header plus the data rows. I subtract one. That is the number of photos the GPU described. I compare it to the jpg, jpeg, and png keys under images/sample, not to every object in the folder. A heic in that prefix will not have a row. Fewer rows than those supported keys means a skipped extension or the wrong stem. More rows than I expected means extra photos were already in the prefix. This program writes the CSV only after all of the selected photos succeed, so a short file is not a partial crash dump from the middle of the GPU loop.

If I want a local copy, I run aws s3 cp a third time. Same source. The destination is ./descriptions.csv in the current directory. I can open that file and see the same header and the same rows. The copy is optional. The object in the CSV bucket is the one the app reads.

I do not call describe-jobs to validate the schema. SUCCEEDED already told me the container exited zero. The columns and the count are an S3 fact. Logs in /aws/batch/job would show the Wrote line, and only if that job reached STARTING or RUNNING. They are the worker's log. They are not the menu.

The GPU can scale away when the queue goes idle. The CSV stays in the bucket. That file, with those two columns, is what the food app ships against.
