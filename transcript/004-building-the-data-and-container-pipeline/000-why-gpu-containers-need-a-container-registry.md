# Video 000 — Why GPU Containers Need a Container Registry

**Section:** 004 — Building the Data and Container Pipeline
**Lecture#:** 000
**Sheet title:** Why GPU Containers Need a Container Registry
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 004-000-why-gpu-containers-need-a-cont

---

The GPU application now runs as `gpu-teaching:latest` on your laptop. AWS Batch still cannot use that local image.

When Batch places the KodeFood job on a GPU instance, the worker must pull the image over the network before starting it. The worker cannot reach Docker Desktop on your machine. If the pull fails, Python never starts, so there are no captions or CSV.

A container registry is the shared source for those image layers. Local Docker is where we build and test. The registry is where Batch retrieves the program. S3 serves the same durable role for the photos and catalog data.

For this course, the registry is Amazon ECR in your account and region. The job definition stores an image URI. At startup, the EC2 instance authenticates with its instance role and pulls the layers. Only then does it run `python /app/describe_items.py`. Your laptop credentials do not belong on the GPU instance.

Notice the deployment boundary: a successful local build does not change what Batch runs. Only a successful push changes the image available from ECR. If a submitted job still behaves like yesterday’s code, compare the local build with the image that was actually pushed.

Next, we will open that ECR reference and separate its repository, tag, and digest. Those three parts tell us exactly how `:latest` selects a program.

---

## Further reading (not spoken)

- [Amazon ECR User Guide](https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html) — private registries for container images on AWS
- [AWS Batch: Jobs](https://docs.aws.amazon.com/batch/latest/userguide/jobs.html) — jobs pull and run container images on compute environments
- [CNCF: How container registries work](https://www.cncf.io/blog/2022/01/18/how-container-registries-work/) — registry role in cloud-native delivery
