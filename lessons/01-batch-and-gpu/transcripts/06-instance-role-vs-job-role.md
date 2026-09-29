# Video 06 — Instance role vs job role
**Type:** Theory
**Runtime target:** ~3 minutes

---

So, two IAM identities matter on this job, and they belong to different layers.

The instance profile is the role the EC2 host uses. In this course that role is ecsInstanceRole. It can pull the image from ECR and write logs to CloudWatch. It talks to the ECS agent. It is attached to the machine. It cannot read S3. The instance role does not get the images bucket, and it does not get the CSV bucket.

The job role is the role the container task uses. You attach it with jobRoleArn on the job definition. In this course that role is gpu-teaching-batch-job-role. Your Python uses it when it calls AWS. It can read the images bucket and write the CSV. It is attached to the application process inside Docker, not to the host. Lesson seven is where both of these get wired. If a name in an older note disagrees, verify the ARN with describe-job-definitions.

Two roles exist so the duties stay split. The machine that downloads Docker layers should not automatically read every S3 bucket in the company. The app that reads vendor photos should not be able to launch EC2. If one role is wider than the work, a bug in the image has a smaller blast radius.

Follow one boot. The instance starts. The instance role authenticates to ECR, including the call batchGetImage, and the layers download. The container starts. AWS injects the job role credentials into the task environment. When the code calls boto3, client s3, get_object, that call is judged against the job role. The same role is what allows the write of the CSV. If the job role is missing, the GPU can still come up. CUDA reports true. Then the first photo fails with AccessDenied. The log is S3, not PyTorch. A job definition with no job role reaches the GPU and fails on the first GetObject. Revision two of gpu-teaching-caption-job is that revision. Seeing a GPU is the instance, the image, and the driver. Touching the vendor's photos is the job role.

CloudWatch can still receive that AccessDenied line, because ecsInstanceRole is allowed to write logs even while the job role is missing. Until describe-job-definitions shows a job role ARN, the CSV write is not allowed.

Spot is the default buy for this GPU, and it can be unavailable. On demand is the fallback, and a quota of zero can make that fallback look healthy while every job sits still. That trap is next.
