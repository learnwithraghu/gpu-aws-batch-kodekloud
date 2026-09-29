# Video 01 — Why ECR exists for Batch
**Type:** Theory
**Runtime target:** ~3 minutes

---

Hello. Let's talk about why Batch needs a private registry.

Amazon Elastic Container Registry is a private Docker registry in your account and in one region. You will hear it called ECR. It stores layered images, the filesystem slices plus the metadata Docker needs to start a container. You address an image with a URI. You can also address the exact bytes with a digest.

AWS Batch needs that registry because the worker is an EC2 instance. At task start it pulls the image over HTTPS. It cannot reach the Docker daemon on your laptop. No pull means no container, and no container means no job. The job definition stores the image URI. When the job starts, the instance authenticates with its instance role, pulls the layers, and only then starts the container.

Your program is inside those layers, the image you built in lesson three. That program captions a KodeFood vendor folder and writes accept or reject into the catalog CSV. If gpu-teaching:latest is missing from the repository, the script never starts. A green docker build on the laptop cannot fill that gap. This lesson is the publish step between that build and any GPU submit.

In this course the URI has a fixed shape. It starts with your account id, then .dkr.ecr.ap-northeast-1.amazonaws.com/gpu-teaching:latest. The repository name is gpu-teaching. The tag is latest. The region inside that host name is Tokyo, ap-northeast-1, the same region as the rest of this pipeline. On the laptop, Docker can show the image as gpu-teaching:latest. Batch does not see that local name. The cluster only sees the copy you publish into this private registry. Private means the layers live in your account, not on a public hub.

That gap is the failure after a clean local build. The image exists on the machine that ran docker build, and the queue still has nothing to pull. A wrong account id in the host, a different region in the registry name, or an empty repository stops the job before your script runs. The URI in the job definition is the contract with the registry.

Next we split that string into the repository, the image, the tag, and the digest.
