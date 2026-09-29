# Video 05 — Job definition as contract
**Type:** Theory
**Runtime target:** ~3 minutes

---

Okay. A job definition is a registered template. Which image, how much CPU, memory, and GPU, which IAM role the container assumes, and what command starts by default. It is not one run. It is the spec many runs share. Submit usually passes the name gpu-teaching-caption-job, and Batch picks the highest active revision. In this course you do not pin revision one or two.

The template exists so every submit does not retype dozens of fields. Platform teams can say caption jobs always use this image, this GPU size, and this S3 role. Runs only vary the day's inputs through overrides in lesson eight.

Read the course card. Name gpu-teaching-caption-job. Image is the ECR URI from lesson four, gpu-teaching tag latest. vCPU is four, the whole g4dn.xlarge. Memory is twelve thousand two hundred eighty-eight mebibytes. Sixteen thousand three hundred eighty-four will not place. The host has sixteen gibibytes, and ECS keeps some for the OS and agent. Resource requirements are four vCPUs, that memory, and GPU one. GPU one tells the scheduler to place only where a GPU is free.

The job role ARN is gpu-teaching-batch-job-role. Without it the container can start and still fail on the first photo download. The default command is a small CUDA check. Lesson eight replaces it with python /app/describe_items.py. Default environment carries S3_BUCKET, S3_CSV_BUCKET, and PYTHONUNBUFFERED one. Log configuration uses awslogs to /aws/batch/job in ap-northeast-1, stream prefix gpu-teaching-caption-job. Logs appear only after STARTING or RUNNING, not while RUNNABLE.

That card is the contract. Your program exits zero when the CSV is written with accepted and rejected rows for KodeFood. Change the S3 prefix or command for one vendor folder with overrides. No new revision. Change the image, GPU, memory, or job role for everyone with a new revision. Overrides cannot repair a broken template.

Registering always creates another revision. Next is why the early numbers bite.
