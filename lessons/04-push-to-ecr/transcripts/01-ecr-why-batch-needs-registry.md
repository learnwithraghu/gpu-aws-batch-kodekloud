# Video 01 — Why ECR exists for Batch
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

Amazon Elastic Container Registry is a private Docker registry in your account and in one region. You will hear it called ECR. It stores layered images, the filesystem slices plus the metadata Docker needs to start a container. You address an image with a URI. You can also address the exact bytes with a digest.

AWS Batch needs that registry because the worker is an EC2 instance. At task start it pulls the image over HTTPS. It can't reach the Docker daemon on your laptop. No pull means no container, and no container means no job. The job definition stores the image URI. When the job starts, the instance authenticates with its instance role, pulls the layers, and only then starts the container. If that pull doesn't happen, the GPU job never begins. No pull, no GPU job.

The sequence on the worker is strict. Batch reads the image URI out of the job definition. The instance role is allowed to pull from ECR in Tokyo. The layers download onto that instance. Only after the layers are there does the container process start. Your program is inside those layers, the image you built in lesson three. If gpu-teaching:latest is missing from the repository, the script never starts. A green docker build on the laptop can't fill that gap. This lesson is the publish step between that build and any GPU submit.

In this course the URI has a fixed shape. It starts with your account id, then .dkr.ecr.ap-northeast-1.amazonaws.com/gpu-teaching:latest. The repository name is gpu-teaching. The tag on the end is latest. The region inside that host name is Tokyo, ap-northeast-1, the same region as the rest of this pipeline. You built the image in lesson three. On the laptop, Docker can show it as gpu-teaching:latest. Batch doesn't see that local name. The cluster only sees the copy you publish into this private registry. Private means the layers live in your account. They are not sitting on a public hub that any machine can pull without permission.

On the screen, picture a Batch instance on the left and an ECR vault on the right. Arrows carry layers from the vault to the instance at the moment the task starts. There is no line from that instance back to your laptop. The laptop is where you built the image. The vault is the only place the job is allowed to fetch it from. The instance role is the credential the worker uses for that fetch.

That gap is the failure after a clean local build. The image exists on the machine that ran docker build, and the queue still has nothing to pull. A wrong account id in the host, a different region in the registry name, or an empty repository stops the job before your script runs. The URI in the job definition is the contract with the registry. Next we split that string into four words that get treated as one: the repository, the image, the tag, and the digest.
