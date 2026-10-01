# Video 000 — From S3 Input to GPU Job: Following the Execution Flow

**Section:** 006 — Running the End-to-End GPU Pipeline
**Lecture#:** 000
**Sheet title:** From S3 Input to GPU Job: Following the Execution Flow
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 006-000-from-s3-input-to-gpu-job--foll

---

Infrastructure is in place. Now follow one vendor folder from object storage all the way to a finished catalog row — not as a diagram, as a sequence you can predict.

Start with bytes on S3. Photos sit under something like `images/<stem>/` in the images bucket. That prefix is the unit of work. Your laptop — or a pipeline step — uploads or syncs those objects first. Batch does not invent the photos; it only captions what is already there.

Next you submit a job to the Spot GPU queue, naming the caption job definition. At submit time you point the container at that stem: buckets, `IMAGE_PREFIX`, batch size, and the command `python /app/describe_items.py`. Batch accepts the submission and begins finding capacity in the compute environment behind the queue.

When an instance is up and the container starts, the job role lets the process list and download under that prefix, run BLIP on the GPU, and write `descriptions/<stem>/descriptions.csv` to the catalog bucket. Logs land in CloudWatch under `/aws/batch/job`. Your laptop can poll job status without ever sitting inside the container.

At larger scale, marketplace catalog work often follows the same shape DoorDash engineering describes: durable storage in, async compute, structured catalog out. Ours is similar, compressed to one folder and one CSV so you see every hop. Further reading points at their blog for that wider context.

Hold the order in your head: S3 input ready, submit with overrides, Batch places on GPU capacity, container reads and writes S3, you read the CSV. If any hop is skipped — empty prefix, wrong queue, stale image — the failure mode changes.

Next we slow down on the status field itself — the lifecycle from SUBMITTED through SUCCEEDED — so you know what each state is allowed to mean.

---

## Further reading (not spoken)

- [AWS Batch: Submitting a job](https://docs.aws.amazon.com/batch/latest/userguide/SubmitJob.html) — submit API and parameters
- [Amazon S3: Organizing objects with prefixes](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-prefixes.html) — prefix as the work unit
- [DoorDash Engineering Blog](https://doordash.engineering/blog/) — marketplace catalog and data pipeline context
