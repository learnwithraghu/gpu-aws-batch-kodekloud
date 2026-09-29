# Video 02 — Container overrides
**Type:** Theory
**Runtime target:** ~3 minutes

---

Okay, so a container override is a per-submit patch to the job definition. On submit-job it is the containerOverrides object. This one job can use a different command and environment without registering a new revision.

Overrides exist because one Docker image serves many vendor folders. Rebuilding or re-registering for every IMAGE_PREFIX is slow and easy to get wrong. The job definition stays the platform template: image URI, GPU, memory, job role. The override holds the run parameters: which S3 prefix, which buckets, how many photos the GPU holds at once.

You submit to BATCH_JOB_DEFINITION by name. Batch picks the highest active revision from lesson 07. Use that revision—broken ones never place or lack S3 and logs. The template already asks for the GPU and memory the instance can place. The override does not repeat those numbers.

For the sample folder the command is python /app/describe_items.py. That replaces the default CUDA check. Environment has four pairs. S3_BUCKET and S3_CSV_BUCKET from the env file. IMAGE_PREFIX images/sample, matching what lesson six synced. BATCH_SIZE 8, how many photos fit on the T4 in one pass. Eight is not the number of output files. One folder still becomes one CSV with accepted and rejected rows. The job name is describe-items-sample. photos.py reads the buckets and IMAGE_PREFIX. describe_items.py reads BATCH_SIZE and defaults to eight if it is missing. Leave out IMAGE_PREFIX and the process cannot list a folder.

A second KodeFood vendor only changes the run parameters. IMAGE_PREFIX becomes images/vendor-b, and the job name moves with the stem. Image, GPU, memory, and revision stay the same.

Overrides cannot repair the template. Wrong memory, missing GPU, bad image URI, or missing job role live in the definition. Sixteen thousand three hundred eighty-four mebibytes is the classic memory mistake, and an override will not shrink it. Register a new revision when the image, GPU, memory, or role should change for every run. Use an override when only this folder's command or environment should change.

The status path from SUBMITTED through SUCCEEDED is next.
