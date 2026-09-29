# Video 04 — Build for linux/amd64
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

The flag --platform linux/amd64 tells docker build to produce an x86_64 image, including when your laptop is ARM. Batch's machine for this course is a g4dn.xlarge, and that instance is x86_64. The image and the instance have to agree on the architecture, or the process never starts. The Python can be perfect, the pin can be perfect, and the wrong binary format still fails on the host.

Apple Silicon laptops default to arm64 when you build and you don't name a platform. That default is reasonable for a container you'll run locally on the Mac. It's the wrong default for this job. An arm64 image pushes to ECR cleanly. The registry stores layers. It doesn't execute them. The failure shows up later, at job time, when the g4dn pulls the image and can't run it. Push succeeded, so the console looks healthy, and the job is the first place the mismatch appears. That delay is why the flag belongs on the build command every time, not as a guess after a red job.

Think of a plug. The appliance is the same design, and the wall socket is a different physical connector. An EU plug and a US socket don't become compatible because the device powered on at the factory. arm64 and the g4dn are that pair. linux/amd64 is the connector the instance accepts. You say it on the command line so Docker doesn't follow the laptop's own architecture.

The command you'll run is docker build, then --platform linux/amd64, then -t gpu-teaching:latest, then a dot for the repo root. The tag is the local name. The platform is the part Batch cares about when the image finally runs. Leave the flag off on an M1, and the tag gpu-teaching:latest can still look fine in docker images while hiding an arm64 build. The tag string doesn't tell you the architecture. You have to have asked for linux/amd64 when you built.

When the architecture is wrong, your program doesn't get a turn. python /app/describe_items.py never starts. You won't see Device followed by cuda, and you won't see a new descriptions.csv, because the process didn't reach main. There's no caption bug to chase in photos.py. The fix is a rebuild with --platform linux/amd64 and a push of those layers. An arm64 image can sit in ECR the whole time, a publish that succeeded, until a g4dn.xlarge is the machine that has to execute it. The instance type doesn't translate the binaries.

On the screen, put an M1 laptop on the left and a g4dn on the right. One arrow is an amd64 image, and it lands green on the instance. A second arrow is an arm64 image. It passes through ECR with a check mark, then hits a red X at run time on the g4dn. The check mark on the push is the trap.

The platform flag sits on the build command. Next you'll see why the Dockerfile installs requirements before it copies the Python files, and why that order turns a code change into a fast rebuild.
