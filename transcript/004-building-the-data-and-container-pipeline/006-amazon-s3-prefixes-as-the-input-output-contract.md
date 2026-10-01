# Video 006 — Amazon S3 Prefixes as the Input/Output Contract

**Section:** 004 — Building the Data and Container Pipeline
**Lecture#:** 006
**Sheet title:** Amazon S3 Prefixes as the Input/Output Contract
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 004-006-amazon-s3-prefixes-as-the-inpu

---

Two buckets give you places to put data. Prefixes decide which objects this job is allowed to see.

S3 keys are flat strings. `images/sample/bowl.jpg` is not a filesystem folder — tools just group on the slash. Our application still treats `images/<stem>/` as a folder contract. `photos.py` lists with `IMAGE_PREFIX`. Only keys under that prefix become caption work. Photos at the bucket root, or under another stem, are invisible to a job aimed at `images/sample`.

The output key is derived from the same stem. `images/sample` becomes `descriptions/sample/descriptions.csv` in the CSV bucket. One folder in, one catalog file out. A second successful run overwrites the same object so the catalog reflects the latest good job for that vendor stem.

This is why upload path and submit override must agree. Sync photos to `images/vendor-b`, then submit with `IMAGE_PREFIX=images/sample`, and you get a healthy container staring at an empty list — or the wrong list. The GPU can be fine. The contract was wrong.

Supported extensions are part of that contract too. The code keeps `.jpg`, `.jpeg`, and `.png`. A GIF or HEIC in the folder is skipped without a row. If you expect thirty rows and get twenty-eight, check extensions before blaming CUDA.

So the data plane is now clear: ECR for the program, S3 prefixes for input and output. What still missing is the scheduler that ties them to a GPU — compute environments, queues, and job definitions.

How does AWS Batch find a machine, attach the right roles, and start that container on a real GPU? That is section five — building the Batch infrastructure.

---

## Further reading (not spoken)

- [Amazon S3: Organizing objects using prefixes](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-prefixes.html) — prefixes as logical folders
- [Amazon S3: Listing objects](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ListingKeysUsingAPIs.html) — how jobs discover keys under a prefix
- [AWS Batch: Passing sensitive data / environment to jobs](https://docs.aws.amazon.com/batch/latest/userguide/job_env.html) — runtime parameters such as IMAGE_PREFIX
