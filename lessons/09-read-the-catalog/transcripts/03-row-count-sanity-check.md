# Video 03 — Row count sanity check
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

The row check compares two counts. On one side, the data rows in the CSV. On the other side, the supported image keys under the prefix. Supported means jpg, jpeg, and png. wc -l on the file counts the header plus the data rows. Subtract one for the header. That number is how many photos the GPU described. It is not how many objects sit in the folder, and it is not how many CSVs were written. There is still one CSV.

The check matters before anyone trusts the captions. Fewer data rows than supported keys means something was skipped, or you counted the wrong stem. More data rows than you expected means extra photos were in the prefix, often photos lesson six already uploaded and you did not notice. A merchandiser should not discover that by reading the menu.

This design writes the file only after every selected photo has a sentence. A failure in the middle should not leave a partial catalog at descriptions, then the stem, then descriptions.csv. If you see a short file, do not assume a crash wrote half the rows. Look for skipped extensions, a wrong IMAGE_PREFIX, or a prefix that was not the folder you think you synced. The empty case is louder. The program prints Found 0 images and exits with No images to describe, and it does not write a header-only success file for that. Exit code one is FAILED, and the log group /aws/batch/job only has those lines after STARTING or RUNNING. A job stuck in RUNNABLE writes nothing, and that stuck state is Spot capacity or the on-demand G and VT quota, not a short CSV.

Take a concrete mismatch. You list about thirty keys in the folder and you count twenty-eight data rows. The two missing names are often a heic, or some other extension the lister drops, or a prefix typo that mixed two folders. The lister keeps jpg, jpeg, and png only, and it sorts them so the CSV order stays stable between runs. Other files in the prefix do not get rows. That is a feature of the contract, and it looks like data loss if you compare against every key S3 shows.

The sample key the app reads is descriptions/sample/descriptions.csv in the CSV bucket. The header must still be image_s3_uri and item_description. BATCH_SIZE eight changes how many photos share one GPU pass. It does not change the row rule. Thirty photos become groups of eight, eight, eight, and six, and then one file. The submit that produced it used gpu-teaching-caption-job by name, highest active revision, command python /app/describe_items.py, on gpu-teaching-gpu-smoke-queue-spot in ap-northeast-1.

On the screen, two numbers sit side by side with an equals sign between them. One number is wc -l minus one. The other is the count of jpg, jpeg, and png keys under the prefix.

When a count fails, the next question is what you rebuild, what you upload, and what you submit again.
