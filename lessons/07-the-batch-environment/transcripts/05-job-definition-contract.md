# Video 05 — Job definition as contract
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

A job definition is a registered template. It answers a fixed set of questions. When Batch runs this kind of work, which container image, how much CPU, memory, and GPU, which IAM role the application inside the container assumes, and what command starts by default. It is not one run. It is the spec many runs share. Like a job description posted for a role, not one person's first morning. Batch stores it by name and by revision. Submit usually passes the name gpu-teaching-caption-job, and Batch picks the highest active revision. You can pin a revision, and in this course you do not pin revision one or revision two.

The template exists so every submit does not retype dozens of fields. Without it, one person asks for too much memory, another forgets the GPU, a third points at a test image. Platform teams can say caption jobs always use this image, this GPU size, and this S3 role. Application runs only vary the inputs for that day, through container overrides in lesson eight.

Read the course template as a filled-in card. The name is gpu-teaching-caption-job. The image is the ECR URI from lesson four, gpu-teaching, tag latest. vCPU is four, the whole g4dn.xlarge, so placement matches one machine. Memory is twelve thousand two hundred eighty-eight mebibytes. Sixteen thousand three hundred eighty-four will not place on this instance type. The host has sixteen gibibytes, and ECS keeps some for the operating system and the agent. Resource requirements are four vCPUs, that memory value, and GPU equals one. GPU equals one is what tells the scheduler to place the job only where a GPU is free.

The job role ARN is gpu-teaching-batch-job-role. Without it, the container can start and still fail on the first photo download. The default command is a small CUDA check, Python minus c, import torch, print whether torch dot cuda dot is_available. Lesson eight replaces that command with python slash app slash describe_items.py. The definition also carries default environment for the two bucket names, S3_BUCKET and S3_CSV_BUCKET, and PYTHONUNBUFFERED set to one so print lines show up while the job runs. Log configuration uses the awslogs driver, the group slash aws slash batch slash job, the region ap-northeast-1, and the stream prefix gpu-teaching-caption-job. Those logs appear only after the job reaches STARTING or RUNNING. They do not appear while it sits in RUNNABLE.

That card is the contract. Batch tries to run a container that honors it. Your program exits zero when the CSV is written. Overrides and revisions are the decision to memorize. Change the S3 prefix or the command for one vendor folder, and you use container overrides on submit-job. No new revision. Change the image URI, the GPU count, the memory, or the job role for everyone, and you register a new revision. Overrides cannot repair a broken template. If the definition still asks for sixteen thousand three hundred eighty-four mebibytes, or omits jobRoleArn, every run fails the same way.

On the screen, the left panel is the job definition, the field list you just heard, sitting still. The right panel is one run, a job ID and a status timeline, with a small overrides note stuck only on the command and the environment. Arrows leave the template toward many job icons, one per vendor folder.

Registering that template always creates another revision number. The next clip is why the early numbers are the ones that bite.
