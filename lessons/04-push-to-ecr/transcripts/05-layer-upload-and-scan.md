# Video 05 — Layer upload and scan on push
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

The first push of this image is large. It's a CUDA and PyTorch image, several gigabytes, about three point eight gigabytes in this course. Most of that weight is the base image and the pip layers. The CUDA user-space libraries and PyTorch dominate the upload. Your own scripts sit in a thin layer on top, so they are a small slice of those bytes.

After a code-only change, Docker and ECR reuse the layers that didn't change. If you only edit photos.py or describe_items.py, the base and the pip layers are already in the repository. Only the thin top layers upload. That's why the first push is slow and a script-only push is quick. It's the same idea as the build-layer caching you saw in lesson three. ECR doesn't need a second copy of a layer it already stored.

On the screen, picture a progress bar. The first push fills the whole bar, about three point eight gigabytes, layer after layer, while the CUDA and PyTorch pieces go up. The second push, after you changed only the scripts, shows most of that bar as already present. A short stretch at the end is the new top layers. The clock on that second push is much shorter, and the repository still has one tag, latest, pointed at the new digest.

Scanning is separate from the upload size. This course creates the repository with scanOnPush set to true. After a push, ECR can flag known CVEs in operating system packages and in language packages. That helps you notice a vulnerable base layer. Treat the scan as a hygiene signal. It doesn't guarantee the job will work, and it doesn't guarantee the model will run. It doesn't replace pinning dependencies. It doesn't replace reading the job logs when the caption job fails. A clean scan can still be a caption job that fails. A finding in the scan can still be an image you go ahead and run, once you've read the finding. You use the scan to notice a vulnerable base layer. You use the job logs to see whether the model ran.

Say the first push finished this morning. describe-images shows a pushed time and a size on the order of three point eight gigabytes. This afternoon you change a line in describe_items.py, you rebuild, and you push again. The CUDA and PyTorch layers are already in ECR from the morning, and Docker can reuse them from the local build cache too. The afternoon push sends the new script layer. latest moves to the new digest. The heavy layers stay put. If you were waiting for another full three point eight gigabyte upload, the short push is the healthy one. Layer reuse is doing what it's for.

The flag belongs on the repository, set when you create it. The create command passes image-scanning-configuration scanOnPush=true. If gpu-teaching already exists, you describe it and you leave it. The scan can flag a CVE after the push, and the first upload is still about three point eight gigabytes either way.

Next you'll log Docker in and push gpu-teaching:latest. Watch the first upload take the full size, and then use describe-images to see the pushed time and the size ECR stored.
