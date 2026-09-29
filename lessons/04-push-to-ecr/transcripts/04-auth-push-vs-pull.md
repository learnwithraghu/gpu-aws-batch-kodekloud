# Video 04 — Push auth vs pull auth
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

Pushing to ECR and pulling from ECR are two different logins, on two different machines, with two different lifetimes.

On your laptop, you are the developer. You run aws ecr get-login-password, and that command prints a short lived password. You pipe it into docker login. Docker uses that password for about twelve hours. The identity behind the password is your IAM user or role, and that identity needs push permissions on the repository. When the twelve hours are up, the login expires. An expired login fails the push. Docker will tell you the login expired. You run get-login-password and docker login again. You don't bake a new long lived key to get around it.

On the GPU box, nobody types a password. The EC2 instance profile in this course is ecsInstanceRole. That role needs permission to pull from ECR. At task start the instance uses the role, pulls the layers for gpu-teaching:latest, and starts the container. Your laptop credentials are not on that machine. If you copied an access key into the instance to make a pull work, you have left the model this course uses.

There is a third place keys must not go. Never bake long lived AWS keys into the image. Image layers keep history. A key copied into a layer can leak when someone pulls the image or reads an old layer. Login passwords are temporary. Instance roles are the durable pull path. Roles can be rotated without rebuilding gpu-teaching. A key inside the image cannot.

When the push fails after the laptop has been idle, trust the twelve hour clock before you blame the image. Docker says the login expired. The repository can exist, gpu-teaching:latest can be built locally, and the push still dies until you run aws ecr get-login-password again and docker login again, region ap-northeast-1, against the same registry host. Pull failures show up earlier. The container hasn't started, because the instance couldn't fetch the layers. ecsInstanceRole is the identity ECR checks for that fetch. Refreshing the laptop login doesn't grant pull to the instance. A healthy ecsInstanceRole doesn't grant push to the laptop. Push still needs your IAM user or role, plus a fresh docker login.

On the screen, picture two arrows into the same registry. On the left, a person at a laptop gets a temporary login, pushes layers, and the password dies in about twelve hours. On the right, an EC2 instance with ecsInstanceRole pulls those layers when Batch starts the task. The two arrows don't share a secret. The laptop push doesn't leave your keys sitting on the GPU.

That split matches the registry story. You publish from a place Batch cannot see. The worker pulls with its own role. If the push fails after a quiet afternoon, check the twelve hour login before you blame the Dockerfile. If the job fails before the container starts, check that ecsInstanceRole can pull, because your laptop session is irrelevant on that box. Next we look at what actually uploads, because the first push of this image is huge, and a later code change is not, and we turn on a scan when the repository is created.
