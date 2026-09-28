# Lesson 04 — Theory

You built an image in lesson 03. This lesson puts it where Batch can pull it.

## Image registry role

AWS Batch instances pull container images over the network. They cannot reach Docker on your laptop.

Amazon ECR is a private registry in your account and region. The job definition stores an image URI. At start time, the instance authenticates (via its instance role), pulls layers, and then starts the container. No pull, no GPU job.

## Repository vs image vs tag

| Term | Example | Meaning |
|------|---------|---------|
| Repository | `gpu-teaching` | Named place that holds images |
| Image | Content addressed by digest | The actual layers (filesystem + metadata) |
| Tag | `latest` | A movable label pointing at one digest |

`666…dkr.ecr…/gpu-teaching:latest` means “whatever digest `latest` currently points to in that repository.” Pushing again moves the tag. Digests stay immutable.

## Mutable tags and reproducibility

`:latest` is convenient for a course: rebuild, push, submit, and the next job picks up the new code without editing the job definition.

In production, teams often pin a digest or an immutable version tag (`v3`, git sha) so yesterday’s successful job can be reproduced exactly. Mutable `:latest` means “whatever was pushed last,” which is easy to teach and easy to surprise yourself with.

## Auth model

**Laptop push:** `aws ecr get-login-password` prints a short-lived password. Docker uses it for about 12 hours. Expired login fails the push; run login again.

**Instance pull:** the EC2 instance profile (`ecsInstanceRole` in this course) needs permission to pull from ECR. Your laptop credentials are not on the GPU box.

Never bake long-lived AWS keys into the image. Login passwords are temporary; instance roles are the durable pull path.

## Layer upload cost

The first push of a CUDA+PyTorch image is large (several GB). Most of that is base and pip layers.

After a code-only change (`photos.py` / `describe_items.py`), Docker and ECR reuse unchanged layers. Only the thin top layers upload. That is why a first push is slow and a script-only push is quick — same idea as build-layer caching in lesson 03.

## Scan on push (course default)

This course creates the repository with `scanOnPush=true`. ECR can flag known CVEs in OS and language packages after a push.

Scanning helps you notice vulnerable base layers. It does not replace pinning dependencies or reading job logs when the caption job fails. Treat it as a hygiene signal, not a guarantee the model will run.
