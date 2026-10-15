# Video 000 — From S3 Input to GPU Job: Following the Execution Flow

**Section:** 006 — Running the End-to-End GPU Pipeline
**Lecture#:** 000
**Sheet title:** From S3 Input to GPU Job: Following the Execution Flow
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 006-000-from-s3-input-to-gpu-job--foll

---

The infrastructure is ready. Now let’s follow one vendor folder from upload to result.

Why do this slowly? Because when this kind of pipeline breaks in a real company, it rarely breaks everywhere at once. It breaks at one hop. If you understand the hops, you know where to look first.

Start at the input. A vendor folder lands in S3. That folder is the unit of work. Batch does not create the images and it does not invent the workload. It processes what already exists under that input boundary.

Next, a job is submitted. At that point we are simply telling the system, "process this folder." Batch then looks for GPU capacity, starts the container when capacity is available, and lets the application read the images, generate captions, and write back one structured CSV.

So the full pattern is simple: durable input, asynchronous GPU compute, durable output.

DoorDash’s engineering writing points at the same kind of concern. Keep the upload path simple. Hand off the heavy work to an async system. Store the result in a place other systems can read later.

Once you see that flow, the first checks become much clearer. No output file? Check the input and the job result. Job waiting? Think about placement and capacity. Container starts and then fails? That is when logs become useful.

Next, we zoom in on the job lifecycle itself and use each status as a clue.

---

## Further reading (not spoken)

- [AWS Batch: Submitting a job](https://docs.aws.amazon.com/batch/latest/userguide/SubmitJob.html) — submit API and parameters
- [Amazon S3: Organizing objects with prefixes](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-prefixes.html) — prefix as the work unit
- [DoorDash Engineering Blog](https://doordash.engineering/blog/) — marketplace catalog and data pipeline context
