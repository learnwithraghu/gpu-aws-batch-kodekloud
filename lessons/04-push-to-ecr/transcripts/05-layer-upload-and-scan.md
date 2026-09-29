# Video 05 — Layer upload and scan on push
**Type:** Theory
**Runtime target:** ~3 minutes

---

Okay. Let's look at what actually uploads, and what scan on push does.

The first push of this image is large. It is a CUDA and PyTorch image, several gigabytes, about three point eight gigabytes in this course. Most of that weight is the base image and the pip layers. Your own scripts sit in a thin layer on top. Those scripts caption the photos the menu will use, but they are not most of the upload.

After a code-only change, Docker and ECR reuse the layers that did not change. If you only edit photos.py or describe_items.py, the base and the pip layers are already in the repository. Only the thin top layers upload. That is why the first push is slow and a script-only push is quick. It is the same idea as the build-layer caching you saw in lesson three. ECR does not need a second copy of a layer it already stored.

Scanning is separate from the upload size. This course creates the repository with scanOnPush set to true. After a push, ECR can flag known CVEs in operating system packages and in language packages. Treat the scan as a hygiene signal. It does not guarantee the job will work or that the model will run. It does not replace pinning dependencies or reading the job logs when the caption job fails. A clean scan can still fail. A finding can still be an image you run once you have read it.

Say the first push finished this morning. describe-images shows a pushed time and a size on the order of three point eight gigabytes. This afternoon you change a line in describe_items.py, rebuild, and push again. The CUDA and PyTorch layers are already in ECR from the morning. The afternoon push sends the new script layer. latest moves to the new digest. The heavy layers stay put. If you were waiting for another full three point eight gigabyte upload, the short push is the healthy one.

The flag belongs on the repository, set when you create it. The create command passes image-scanning-configuration scanOnPush equals true. If gpu-teaching already exists, you describe it and you leave it. The scan can flag a CVE after the push, and the first upload is still about three point eight gigabytes either way.

Next you will log Docker in and push gpu-teaching:latest. Watch the first upload take the full size, then use describe-images to see the pushed time and the size ECR stored.
