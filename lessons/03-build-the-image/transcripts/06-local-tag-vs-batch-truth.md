# Video 06 — Local tag vs what Batch runs
**Type:** Theory
**Runtime target:** ~3 minutes

---

Okay. Here's the thing about local tags.

docker images shows tags on your machine. When you ask it for gpu-teaching, you should see the local tag gpu-teaching:latest, and the image is several gigabytes, because the CUDA base and the Python packages are in those layers. That tag is a name in your local Docker daemon. AWS can't see it. Batch doesn't pull from your laptop. The workers pull over the network from ECR, in this course in ap-northeast-1. Until lesson four pushes the tag, the registry and your laptop are disconnected.

Two clocks cause the stale captions you already met in the program lesson. "I built today" can be true on the laptop and false for the job. ECR's latest can still be yesterday's scripts. The job definition points at whatever latest, or whatever digest, already lives in the registry. If that object is yesterday's bake of describe_items.py, the new prompt in your editor never runs. The CSV looks like the build failed to pick up your edit. The build worked. The push didn't happen, or it went somewhere the job definition doesn't read.

The check this lesson uses is docker images gpu-teaching. You want one local line, the tag gpu-teaching:latest, several gigabytes. No line means the build didn't tag the name you think it tagged. A line means this laptop's daemon has the image. Submit images/sample while ECR still holds yesterday's latest, and descriptions/sample/descriptions.csv still shows yesterday's sentences. The new layers never left the machine.

Keep the local tag and the image Batch will run as two different facts until the push succeeds. Build only, and Batch still launches the previous digest. Build and push, and Batch can pick up the new digest behind the latest tag. The tag name gpu-teaching:latest is allowed to move. The digest underneath it changes when the push completes. Same tag string, new digest, and that new digest is what the next job pulls. Looking at docker images after a local build doesn't tell you which digest the next job will pull.

Lesson four creates the ECR repository if it's not there and pushes this tag. This lesson ends with the image on the laptop, on purpose, so you can see the gap before you close it.

The next clip is the build itself. You'll see the Dockerfile from the top, then docker build with linux/amd64, and the local tag that proves the image exists on this machine only.
