# Video 005 — Designing Storage for Batch GPU Pipelines

**Section:** 004 — Building the Data and Container Pipeline
**Lecture#:** 005
**Sheet title:** Designing Storage for Batch GPU Pipelines
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 004-005-designing-storage-for-batch-gp

---

ECR holds the program, but the GPU instance is temporary. When Batch removes that instance, its local disk disappears. The vendor photos and catalog CSV therefore need durable storage outside the container.

S3 provides that durable side of the KodeFood pipeline. The job downloads images, runs BLIP, and uploads one CSV. A new vendor delivery adds objects under a prefix. We do not rebuild the AMI or container image to add photos. Code changes require a rebuild and push; data changes require an upload.

This course uses two buckets. One stores vendor images and is mostly read by the job. The other stores catalog output, which the job writes and the application reads. One bucket with separate prefixes could also work. Two buckets make the permissions clearer: read from one and write to the other. They also reduce the chance of mixing raw uploads with curated catalog files.

Keep both buckets in the same region as Batch. Cross-region access adds latency and cost. Bucket names must also be globally unique across AWS, so the course names include a stable suffix.

Notice the system boundary. The container image contains CUDA, PyTorch, and our scripts. S3 contains every vendor folder processed by that same image. If the container finishes but the CSV is missing, inspect the output bucket, key, and write permission before looking at GPU utilization.

We now have durable storage on both sides of temporary compute. Next, we will define the exact S3 prefixes the job reads and writes.

---

## Further reading (not spoken)

- [Amazon S3 User Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html) — durable object storage for pipeline I/O
- [AWS well-architected: Storage](https://docs.aws.amazon.com/wellarchitected/latest/framework/storage.html) — separating durable data from ephemeral compute
- [Airbnb Engineering: Bighead](https://medium.com/airbnb-engineering/bighead-airbnbs-end-to-end-machine-learning-platform-f32564349eef) — ML platform separation of data and model concerns
