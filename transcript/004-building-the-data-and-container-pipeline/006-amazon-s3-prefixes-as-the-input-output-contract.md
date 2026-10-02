# Video 006 — Amazon S3 Prefixes as the Input/Output Contract

**Section:** 004 — Building the Data and Container Pipeline
**Lecture#:** 006
**Sheet title:** Amazon S3 Prefixes as the Input/Output Contract
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 004-006-amazon-s3-prefixes-as-the-inpu

---

The two buckets provide durable locations. Prefixes define the objects for one KodeFood job.

S3 keys are flat strings. `images/sample/bowl.jpg` is not a filesystem path, even though tools display slashes like folders. Our application treats `images/<stem>/` as a logical input contract. `photos.py` lists objects using `IMAGE_PREFIX`, so only matching keys become caption work.

For example, a job with `IMAGE_PREFIX=images/sample` cannot see photos at the bucket root or under another vendor stem. The output key comes from the same stem: `images/sample` maps to `descriptions/sample/descriptions.csv` in the CSV bucket. One input prefix produces one catalog file. A later successful run overwrites that object with the latest result.

The upload path and submit override must agree. If photos are under `images/vendor-b` but the job receives `IMAGE_PREFIX=images/sample`, the container may start normally and still find no work, or process the wrong vendor. That is a data-contract problem, not a GPU problem.

File extensions are also part of the contract. The code accepts `.jpg`, `.jpeg`, and `.png`. It skips GIF and HEIC objects without creating rows. If thirty uploaded files produce twenty-eight rows, check the extensions and prefix before investigating CUDA.

We can now trace the data plane: Batch pulls the program from ECR, reads images from one S3 prefix, and writes one CSV to the derived output key. The next section adds the scheduler: compute environments, queues, roles, and job definitions that place this container on a GPU.

---

## Further reading (not spoken)

- [Amazon S3: Organizing objects using prefixes](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-prefixes.html) — prefixes as logical folders
- [Amazon S3: Listing objects](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ListingKeysUsingAPIs.html) — how jobs discover keys under a prefix
- [AWS Batch: Passing sensitive data / environment to jobs](https://docs.aws.amazon.com/batch/latest/userguide/job_env.html) — runtime parameters such as IMAGE_PREFIX
