# Video 02 — Repository, image, tag, digest
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

A repository in ECR is a named place that holds images. In this course the name is gpu-teaching. It works like a GitHub repository name. It stays put while many pushes land inside it over the life of the course.

An image is the actual content. It is an ordered stack of layers, filesystem diffs, plus metadata. ECR identifies that content with a digest, a sha256 hash of the bytes. The digest is content addressed, so the same bytes always produce the same digest. A digest is immutable. You cannot edit the layers behind sha256 and keep the same hash.

A tag is a human readable pointer to one digest at a time. latest is the tag this course uses. You will also see tags like v1 or git-abc123 in other systems. A tag can move. Unless you turn on policies that freeze tags, pushing again can point latest at a new digest. The old digest does not change. It stays in the repository until something deletes it.

People flatten those three words into one sentence. They say they pushed the image to ECR, and they mean they uploaded a layer stack and moved a tag. That shorthand is fine until something breaks. On an incident you need the digest that ran, not the slogan that you use latest. If a job id comes back as abc, the question is which digest that job pulled, because latest may already point somewhere else.

Here is the course story. The full string is your account id, then .dkr.ecr.ap-northeast-1.amazonaws.com/gpu-teaching:latest. That means whatever digest latest currently points to in the gpu-teaching repository. On Monday you push, and latest points at digest A. On Tuesday you push again, and latest moves to digest B. Digest A is still there if you name it directly. The job definition image field is still the tag form of that URI. You don't edit it. On Wednesday a new job starts, the scheduler resolves the tag to a digest at pull time on the instance, and the job runs B.

The job definition doesn't store the layer bytes. It stores a string in the image field, usually the tag form, because that's what you'll register later for gpu-teaching:latest. At pull time, on the instance, the scheduler resolves that tag to the digest it points at right then. Submit with the digest and you've named the bytes. A later move of latest leaves that request on digest A. Leave the tag in the string, and Wednesday's job follows the arrow to B. Same repository. Two ways to ask. The course uses the tag so the next push is what the next job gets.

On the screen, picture one box labeled gpu-teaching. Inside it, two boxes labeled digest A and digest B. An arrow labeled latest starts on A. After the second push, the arrow moves to B. A does not disappear. Only the label moved.

Pushing again moves the tag. Digests stay immutable. That moving label is convenient, and it is also how you surprise yourself. Next we stay on latest, and we talk about when a course should let that tag move and when a production system should pin the digest instead.
