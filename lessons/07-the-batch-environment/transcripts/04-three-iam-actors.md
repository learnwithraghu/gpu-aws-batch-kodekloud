# Video 04 — Three IAM actors
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

An IAM role is a set of temporary credentials that a service or an instance assumes when it calls another AWS API. One Batch GPU job uses three principals, often in the same minute, and they do not share a policy.

The first is the Batch service-linked role, AWSServiceRoleForBatch. Batch itself assumes it to create and scale ECS and EC2 capacity on your behalf. Batch creates that role the first time you make a compute environment. If the create complains that the role is missing, you call create-service-linked-role with the service name batch.amazonaws.com, once. This role does not read your photos.

The second is the instance profile, ecsInstanceRole. The EC2 host assumes it. Its job is to pull the image from ECR and to write container logs to CloudWatch. The managed policy attached to it is AmazonEC2ContainerServiceforEC2Role. The trust policy allows ec2.amazonaws.com to assume it. You can check that the profile exists with get-instance-profile and the name ecsInstanceRole. This host role does not get S3 access. The machine that runs Docker should not automatically hold every bucket in the account.

The third is the job role, gpu-teaching-batch-job-role, stored on the job definition as jobRoleArn. The container task assumes it. The trust policy allows ecs-tasks.amazonaws.com. This role is the catalog's S3 identity. It can list the images bucket and the captions bucket. It can get objects in the images bucket. It can get and put objects in the captions bucket. That is how describe_items.py reads photos and writes the CSV. You check it with get-role and the name gpu-teaching-batch-job-role. The ARN goes into the env file as BATCH_JOB_ROLE_ARN. An empty job role means the GPU can start and the first S3 call still fails.

Least privilege is why there are three. The Python process does not need permission to launch EC2. The host does not need permission to put a CSV. Splitting them limits the blast radius when code is wrong or a credential leaks. The same split is why a platform gives each service its own identity instead of one shared admin role.

The failures come in three shapes. Missing or wrong service-linked role, and the compute environment goes INVALID. Nothing scales. Read statusReason. Instance profile missing ECR rights, and the image pull fails in STARTING. The log mentions CannotPullContainerError. Job definition missing the job role, and the container starts, CUDA works, and the first get object throws AccessDenied. That one is expensive. The GPU minute meter is already running.

Walk one job in order. Batch, using the service-linked role, scales the compute environment. EC2 boots with ecsInstanceRole and pulls the image. The task starts with gpu-teaching-batch-job-role. describe_items.py reads the photos. Three badges, three arrows, never swapped. Lesson seven stores jobRoleArn on the job definition. In the teaching account, revision three and later is where that field is actually filled in. You verify it with describe-job-definitions, not from memory.

On the screen, three boxes in a row. Batch service, EC2 host, container task. Under the host, a policy chip for ECR and logs. Under the task, a policy chip for S3. No line connects the host chip to the bucket.

The template those three actors run from is the job definition. The next clip reads it as a contract: image, memory, one GPU, and the job role.
