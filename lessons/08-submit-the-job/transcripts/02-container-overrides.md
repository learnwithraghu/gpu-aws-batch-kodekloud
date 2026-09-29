# Video 02 — Container overrides
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

A container override is a per-submit patch to the job definition's container spec. On the submit-job API it is the containerOverrides object. It lets this one job use a different command and a different set of environment variables without registering a new revision.

Overrides exist because one Docker image serves many vendor folders. Rebuilding the image, or registering a new job definition, for every IMAGE_PREFIX would be slow and easy to get wrong. The job definition stays the platform template. That template holds the image URI, the GPU count, the memory, and the job role. The override holds the run parameters. Those are which S3 prefix to read, which buckets to use, and how many photos to hand the GPU at once.

The course definition is named gpu-teaching-caption-job. You submit that name, in ap-northeast-1, on the queue gpu-teaching-gpu-smoke-queue-spot, and Batch picks the highest active revision. You do not submit revision one or revision two. The template already asks for one GPU and twelve thousand two hundred eighty-eight mebibytes. The override does not repeat those numbers. It replaces the work for this run.

For the sample folder the command is python, then /app/describe_items.py. That replaces the default CUDA check, which only prints whether torch.cuda.is_available is true or false. The environment is four name and value pairs. S3_BUCKET is the images bucket from the env file. S3_CSV_BUCKET is the CSV bucket. IMAGE_PREFIX is images/sample, and it has to match the prefix lesson six synced. BATCH_SIZE is 8, which is how many photos the GPU holds in one pass. Eight fits the T4 on a g4dn.xlarge. It is not the number of output files. One folder still becomes one CSV. The submit in this course names that run describe-items-sample. The override is one JSON object, a command array plus an environment array of name and value pairs. Those values are not hard-coded in the Python. photos.py reads the two buckets and IMAGE_PREFIX from the environment. describe_items.py reads BATCH_SIZE, and it defaults to eight only if the override left that variable out. Leave out IMAGE_PREFIX and the process cannot list a folder.

A second vendor only changes the run parameters. IMAGE_PREFIX becomes images/vendor-b, and the job name changes with the folder stem. The image, the GPU, the memory, and the revision stay the same.

Overrides cannot repair the template. Wrong memory, a missing GPU, a bad image URI, or a missing job role ARN all live in the job definition. Sixteen thousand three hundred eighty-four mebibytes is the classic memory mistake on this instance type, and an override will not shrink it. You register a new revision when the image, the GPU count, the memory, or the job role should change for every run. You use an override when only this folder's command or environment should change.

On the screen, the job definition card stays still, with image, GPU, memory, and role filled in. A small override note sits on the command and the environment only. Two submit arrows leave that card, one labeled images/sample and one labeled images/vendor-b.

The status path from SUBMITTED through SUCCEEDED is next.
