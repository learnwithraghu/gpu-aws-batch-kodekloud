# Video 04 — Push auth vs pull auth
**Type:** Theory
**Runtime target:** ~3 minutes

---

So, who pushes from the laptop, and who pulls on the GPU box?

Pushing to ECR and pulling from ECR are two different logins, on two different machines, with two different lifetimes.

On your laptop, you are the developer. You run aws ecr get-login-password, and that command prints a short lived password. You pipe it into docker login. Docker uses that password for about twelve hours. The identity behind the password is your IAM user or role, and that identity needs push permissions on the repository. When the twelve hours are up, the login expires. An expired login fails the push. You run get-login-password and docker login again. You do not bake a long lived key to get around it.

On the GPU box, nobody types a password. The EC2 instance profile in this course is ecsInstanceRole. That role needs permission to pull from ECR. At task start the instance uses the role, pulls the layers for gpu-teaching:latest, and starts the container. That is the shared Batch pool KodeFood uses when a vendor folder is waiting. Your laptop credentials are not on that machine. If you copied an access key into the instance to make a pull work, you have left the model this course uses.

Never bake long lived AWS keys into the image either. Image layers keep history. A key copied into a layer can leak when someone pulls the image or reads an old layer. Login passwords are temporary. Instance roles are the durable pull path. Roles can be rotated without rebuilding gpu-teaching. A key inside the image cannot.

When the push fails after the laptop has been idle, trust the twelve hour clock before you blame the image. The repository can exist, gpu-teaching:latest can be built locally, and the push still dies until you run get-login-password and docker login again, region ap-northeast-1, against the same registry host. Pull failures show up earlier. The container has not started, because the instance could not fetch the layers. ecsInstanceRole is the identity ECR checks for that fetch. Refreshing the laptop login does not grant pull to the instance. A healthy ecsInstanceRole does not grant push to the laptop.

You publish from a place Batch cannot see. The worker pulls with its own role.

Next we look at what actually uploads, because the first push of this image is huge, and a later code change is not, and we turn on a scan when the repository is created.
