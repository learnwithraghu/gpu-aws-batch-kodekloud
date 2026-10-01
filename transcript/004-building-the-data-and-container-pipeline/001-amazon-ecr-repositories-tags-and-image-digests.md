# Video 001 — Amazon ECR: Repositories, Tags and Image Digests

**Section:** 004 — Building the Data and Container Pipeline
**Lecture#:** 001
**Sheet title:** Amazon ECR: Repositories, Tags and Image Digests
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 004-001-amazon-ecr--repositories--tags

---

Batch needs a registry. On AWS, our registry is Amazon ECR. Three words get mixed constantly — repository, tag, and digest — so let’s separate them.

A repository is a named place that holds images. In this course that name is `gpu-teaching`. An image is the actual content: layers plus metadata, addressed by a digest — a content hash. A tag is a movable label that points at one digest. When people say `gpu-teaching:latest`, they mean “whatever digest the label `latest` currently points to in that repository.”

Push again and `latest` can move. The old digest still exists as immutable content, but the label walked forward. That is convenient for teaching: rebuild, push, submit, and the next job picks up new code without editing the job definition. It is also easy to surprise yourself. Yesterday’s successful run and today’s submit may not be the same bytes if someone pushed in between.

Production teams often pin a digest or an immutable version tag — a git SHA, `v3`, a build number — so a known-good job can be reproduced exactly. Mutable `:latest` means “whatever was pushed last.” Choose consciously.

Auth splits in two. Your laptop pushes with a short-lived ECR login password. The GPU instance pulls with `ecsInstanceRole`. Never bake long-lived access keys into the image. The first CUDA-plus-PyTorch push is large; later code-only pushes reuse unchanged layers and stay thin.

We will skip the push demos for a moment in this theory track. Ask yourself first: once the program lives in ECR, where do the photos and the CSV live? Storage design is next — two buckets, clear roles, durable I/O for a temporary GPU.

---

## Further reading (not spoken)

- [Amazon ECR: Images](https://docs.aws.amazon.com/AmazonECR/latest/userguide/images.html) — tags, digests, and image manifests
- [Amazon ECR: Private repository concepts](https://docs.aws.amazon.com/AmazonECR/latest/userguide/Repositories.html) — what a repository stores
- [OCI Image Spec](https://github.com/opencontainers/image-spec) — content-addressed image digests in the wider ecosystem
