# Video 000 — Why GPU Containers Need a Container Registry

**Section:** 004 — Building the Data and Container Pipeline
**Lecture#:** 000
**Sheet title:** Why GPU Containers Need a Container Registry
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 004-000-why-gpu-containers-need-a-cont

---

You just containerized the GPU application. On your laptop you can run Docker and see `gpu-teaching:latest`. That is not enough for AWS Batch.

When Batch places a job on a GPU instance, that instance must pull the container image over the network and then start it. The worker cannot reach Docker Desktop on your machine. No registry pull means no container start, which means no captions and no CSV — even if your local build looks perfect.

A container registry is the shared place those workers pull from. Think of it as the durable home for the program, the same way S3 is the durable home for photos. Local disk is for building. The registry is for running.

This pattern is how cloud GPU fleets stay consistent. Platform teams publish job images to a registry so any autoscaled worker can start the same layers. The machine is disposable. The image tag or digest is the contract for “which program runs.”

For KodeFood in this course, that registry is Amazon ECR in your account and region. The job definition stores an image URI. At start time, the EC2 instance uses its instance role to authenticate, pulls the layers, and only then runs `python /app/describe_items.py`. Your laptop credentials never need to live on that GPU box.

Hold a sharp distinction in your head: built locally versus what Batch will run. Those become the same fact only after a successful push. Until then, submitting a job may still pull yesterday’s image — or fail if nothing is there.

That's it here for registries: Batch workers do not inherit your laptop's Docker cache. They pull. Next we open Amazon ECR — repositories, tags, and digests — so you know what `:latest` actually means.

---

## Further reading (not spoken)

- [Amazon ECR User Guide](https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html) — private registries for container images on AWS
- [AWS Batch: Jobs](https://docs.aws.amazon.com/batch/latest/userguide/jobs.html) — jobs pull and run container images on compute environments
- [CNCF: How container registries work](https://www.cncf.io/blog/2022/01/18/how-container-registries-work/) — registry role in cloud-native delivery
