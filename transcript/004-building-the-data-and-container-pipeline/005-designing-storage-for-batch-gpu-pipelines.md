# Video 005 — Designing Storage for Batch GPU Pipelines

**Section:** 004 — Building the Data and Container Pipeline
**Lecture#:** 005
**Sheet title:** Designing Storage for Batch GPU Pipelines
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 004-005-designing-storage-for-batch-gp

---

ECR holds the program. The GPU instance is temporary. When Batch scales in, local disk on that machine is gone. So photos and the catalog CSV cannot live only inside the container.

Object storage is the durable side of the pipeline. The job downloads images, runs BLIP, and uploads one CSV. The next vendor drop is more objects under a prefix — you do not bake photos into the AMI or into image layers. Code changes mean rebuild and push. New photos mean upload only.

This course uses two buckets on purpose. One holds vendor images — mostly read by the job. The other holds catalog output — written by the job, read by the app. You could use one bucket with two prefixes. Separate buckets make IAM easier to explain — read on one, write on the other — and make it harder to mix raw uploads with curated catalog files by accident.

Create them in the same region as Batch. Cross-region traffic adds latency and cost, and it muddies a teaching story that should stay one-region clear. Bucket names are globally unique across AWS, which is why course names usually include a stable suffix so creation does not collide with someone else’s `my-photos`.

Notice the product boundary. The container image is CUDA, PyTorch, and your scripts. S3 is every vendor folder you will ever caption with that same image. Airbnb’s Bighead write-up draws that line at marketplace scale — model packaging versus data — similar to what we are doing, not a copy of their platform. Further reading has the Bighead article when you want their version of the story.

That's it here for storage shape: durable buckets, temporary GPU in the middle. Next — S3 prefixes as the input and output agreement the job lists and writes.

---

## Further reading (not spoken)

- [Amazon S3 User Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html) — durable object storage for pipeline I/O
- [AWS well-architected: Storage](https://docs.aws.amazon.com/wellarchitected/latest/framework/storage.html) — separating durable data from ephemeral compute
- [Airbnb Engineering: Bighead](https://medium.com/airbnb-engineering/bighead-airbnbs-end-to-end-machine-learning-platform-f32564349eef) — ML platform separation of data and model concerns
