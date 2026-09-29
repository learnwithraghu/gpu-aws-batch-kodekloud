# Video 09 — Demo: Batch environment setup
**Type:** Demo  
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

By now you have a container image in ECR, and a folder of photos in S3. Batch still will not start a GPU until three things are registered in this account. A compute environment, the pool of machines. A job queue, where you send the work. And a job definition, the template for the container: which image, how much memory, one GPU, and which role can touch S3.

This clip is the setup, not the job. We look before we create. If the name is already there and it looks healthy, we leave it alone. A second compute environment with a different name is a second pool, and you pay for that pool when jobs land on it.

I'm in the terminal. The region is Tokyo, ap-northeast-1. I source the env file so the account, the image URI, and the job role are already in the shell.

First, the compute environment. The Spot one we use is named gpu-teaching-gpu-smoke-ce-spot. I run describe-compute-environments and pass that name.

What I want back is status VALID. Then I look at the compute resources. The instance type should be g4dn.xlarge. Minimum vCPUs should be zero, so nothing is running while the class is idle. Maximum vCPUs is four, one of those machines. If status comes back INVALID, I read statusReason before I create anything else. A bad subnet, security group, or instance profile shows up there.

If describe comes back empty, the environment does not exist yet, and that is the only time I create it. Same instance type, same vCPU limits, Spot, and the subnet and security group from the course notes. The field I want you to see is the image type, ECS_AL2023_NVIDIA. That AMI already has the NVIDIA drivers on the host. A plain Amazon Linux image on a g4dn can look like a GPU machine and still leave CUDA invisible inside the container. After create, I describe again and wait until status is VALID. That can take a minute or two.

Next, the queue. I describe gpu-teaching-gpu-smoke-queue-spot. I want the state ENABLED and the status VALID. The compute environment order should point at the Spot environment we just checked. Jobs on this queue run on that pool. They do not hop to the on-demand environment because Spot is quiet. If the queue is missing, I create it only after the compute environment is VALID, and I bind it to that environment in the same command.

Last, the job definition, gpu-teaching-caption-job. I describe job definitions, active only, and I look at the highest revision. The image should be the ECR URI we pushed. Memory is twelve thousand two hundred eighty-eight mebibytes. Sixteen thousand will not place on this instance type. Resource requirements should include one GPU and four vCPUs. The job role ARN should be filled in. That role reads the photos and writes the CSV. An empty role means the GPU can start and the first S3 call still fails. Logs should use the awslogs driver and the group /aws/batch/job.

That JSON is the contract from the theory clip, stored in the account. If there is no active revision, or the image, memory, GPU, role, or logs are wrong, I register once. Register always makes a new revision, even when nothing changed, so I do not register just to feel sure. I read the revision number that comes back. When we submit, we pass the name and let Batch pick the highest active revision. We do not pin revision one or revision two.

Three things should be true before I stop. The compute environment status is VALID. The queue is enabled and points at that environment. The job definition has an active revision with one GPU, the right memory, and a job role. Lesson eight is the submit. The overrides on that call choose the vendor folder. The template we just checked chooses the machine.
