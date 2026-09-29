# Video 03 — Row count sanity check
**Type:** Theory
**Runtime target:** ~3 minutes

---

Alright. Before you trust the menu, count the rows. The row check compares two counts. Data rows in the CSV on one side. Supported image keys under the prefix on the other. Supported means jpg, jpeg, and png. wc -l counts header plus data rows. Subtract one for the header. That number is how many photos the GPU described. There is still one CSV. Accepted and rejected both count as rows. A rejected car photo is still a line. KodeFood filters on photo_status later. The row check does not drop rejected rows.

Fewer data rows than supported keys means something was skipped, or you counted the wrong stem. More rows than you expected means extra photos were in the prefix. A merchandiser should not discover that by reading the menu.

This design writes the file only after every selected photo has a sentence and a status. A failure in the middle should not leave a partial catalog. If you see a short file, look for skipped extensions, a wrong IMAGE_PREFIX, or a prefix that was not the folder you synced. Empty is louder. Found 0 images, then No images to describe, and no header-only success file. Exit code one is FAILED. Logs in /aws/batch/job appear only after STARTING or RUNNING. Stuck RUNNABLE writes nothing. That is Spot capacity or the on-demand G and VT quota, not a short CSV.

Concrete mismatch. About thirty keys in the folder, twenty-eight data rows. The two missing names are often a heic or another extension the lister drops. The lister keeps jpg, jpeg, and png only, and sorts them so CSV order stays stable. Other files in the prefix do not get rows. That looks like data loss if you compare against every key S3 shows.

The sample key is descriptions/sample/descriptions.csv. Header must be image_s3_uri, item_description, photo_status. BATCH_SIZE eight changes how many photos share one GPU pass. It does not change the row rule. Thirty photos become groups of eight, eight, eight, and six, then one file. The submit used gpu-teaching-caption-job by name on gpu-teaching-gpu-smoke-queue-spot in ap-northeast-1. The Wrote line in the logs reports accepted and rejected counts for that same file.

When a count fails, next is what you rebuild, upload, and submit again.
