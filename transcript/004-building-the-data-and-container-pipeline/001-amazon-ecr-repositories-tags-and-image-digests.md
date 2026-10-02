# Video 001 — Amazon ECR: Repositories, Tags and Image Digests

**Section:** 004 — Building the Data and Container Pipeline
**Lecture#:** 001
**Sheet title:** Amazon ECR: Repositories, Tags and Image Digests
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 004-001-amazon-ecr--repositories--tags

---

Batch pulls our image from Amazon ECR. Let’s separate three terms that describe what it pulls: repository, tag, and digest.

A repository is a named collection of images. Here, the repository is `gpu-teaching`. The image content consists of layers and metadata. ECR identifies that exact content with a digest, which is a content hash. A tag is a movable label that points to a digest.

So `gpu-teaching:latest` means the digest currently selected by the `latest` tag in that repository. Push a new build with the same tag, and `latest` moves. The earlier digest remains immutable, but the label now selects different bytes.

That behavior is convenient in this course. We rebuild, push, and submit without changing the job definition. It also affects diagnosis. Two jobs submitted against `:latest` may run different image content if a push happened between them.

For repeatable production runs, teams often pin a digest or use an immutable version tag such as a git SHA, `v3`, or a build number. Use `:latest` only when you intend to follow the most recent push.

Authentication also has two paths. Your laptop pushes with a short-lived ECR login password. The GPU instance pulls with `ecsInstanceRole`. Long-lived access keys should never be baked into the image. The first CUDA-plus-PyTorch push is large; later code-only pushes can reuse unchanged layers.

The program now has a durable home. Next, we will give the input photos and output CSV their own durable storage while the GPU instance remains temporary.

---

## Further reading (not spoken)

- [Amazon ECR: Images](https://docs.aws.amazon.com/AmazonECR/latest/userguide/images.html) — tags, digests, and image manifests
- [Amazon ECR: Private repository concepts](https://docs.aws.amazon.com/AmazonECR/latest/userguide/Repositories.html) — what a repository stores
- [OCI Image Spec](https://github.com/opencontainers/image-spec) — content-addressed image digests in the wider ecosystem
