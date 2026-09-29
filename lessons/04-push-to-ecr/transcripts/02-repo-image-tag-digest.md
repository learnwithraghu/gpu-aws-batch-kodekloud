# Video 02 — Repository, image, tag, digest
**Type:** Theory
**Runtime target:** ~3 minutes

---

Okay, so let's split that URI into repository, image, tag, and digest.

A repository in ECR is a named place that holds images. In this course the name is gpu-teaching. It works like a GitHub repository name. It stays put while many pushes land inside it over the life of the course.

An image is the actual content. It is an ordered stack of layers, filesystem diffs, plus metadata. ECR identifies that content with a digest, a sha256 hash of the bytes. The digest is content addressed, so the same bytes always produce the same digest. A digest is immutable. You cannot edit the layers behind sha256 and keep the same hash.

A tag is a human readable pointer to one digest at a time. latest is the tag this course uses. You will also see tags like v1 or a git sha in other systems. A tag can move. Unless you freeze tags with a policy, pushing again can point latest at a new digest. The old digest does not change. It stays until something deletes it.

People say they pushed the image to ECR, and they mean they uploaded a layer stack and moved a tag. That shorthand is fine until something breaks. On an incident you need the digest that ran, not the slogan that you use latest. If a job comes back, the question is which digest that job pulled, because latest may already point somewhere else.

The full string is your account id, then .dkr.ecr.ap-northeast-1.amazonaws.com/gpu-teaching:latest. That means whatever digest latest currently points to in the gpu-teaching repository. On Monday you push, and latest points at digest A. On Tuesday you push again, and latest moves to digest B. Digest A is still there if you name it directly. The job definition keeps the tag form. On Wednesday a new job starts, the scheduler resolves the tag at pull time, and the job runs B. That is the same container KodeFood uses to caption a vendor folder and write photo_status on each row.

Submit with the digest and you have named the bytes. Leave the tag in the string, and Wednesday's job follows latest to B. The course uses the tag so the next push is what the next job gets. Pushing again moves the tag. Digests stay immutable.

Next we stay on latest, and we talk about when a course should let that tag move and when production should pin the digest instead.
