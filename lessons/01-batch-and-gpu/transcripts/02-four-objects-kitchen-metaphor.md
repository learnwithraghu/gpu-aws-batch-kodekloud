# Video 02 — The four Batch objects
**Type:** Theory
**Runtime target:** ~3 minutes

---

Okay, so four objects show up on every Batch diagram, and this course has a real name for each of them.

The compute environment is the rule for which EC2 capacity Batch may start. Instance types. Spot or on demand. The network. Minimum and maximum vCPUs. The machine image, when the job needs a GPU. The Spot environment here is gpu-teaching-gpu-smoke-ce-spot. It may use a Spot g4dn.xlarge in Tokyo, region ap-northeast-1, and it may scale from zero.

The job queue is the line jobs enter when you submit them. A queue does not hold servers. It holds jobs. It is bound to one or more compute environments, with a priority. This course uses gpu-teaching-gpu-smoke-queue-spot, and that queue uses the Spot environment. When a job is waiting, the environment can start an instance. When the queue is empty, minimum vCPUs of zero lets capacity fall away. You pay for the instance only while it is up.

The job definition is a registered template, versioned, and it is not one run. It records the ECR image, CPU, memory, GPU, the job role, the default command, and logging. AWS stores it as a name and a revision. Submit usually passes the name, and Batch picks the latest active revision unless you pin one. Our template is gpu-teaching-caption-job. Read it as, run gpu-teaching, colon, latest, one GPU, twelve thousand two hundred eighty-eight mebibytes, a job role that can touch S3, and a default command that checks CUDA. Revision one asks for sixteen thousand three hundred eighty-four mebibytes. Revision two has no job role. Revision three and later place and can write the CSV.

The job is one execution of that template. It has its own job ID, a status timeline from SUBMITTED through to SUCCEEDED, and optional overrides for this run only. Tonight's job is the prefix images/sample, with overrides that point describe_items.py at that folder.

Platform teams own compute environments and queues. Application teams own job definitions and submits. Changing the Docker image for everyone means a new revision. Changing only this folder's S3 prefix means a submit override. Three names from older examples are not resources here. gpu-teaching-ce, gpu-teaching-queue, and gpu-teaching-job-def. Do not create them.

The kitchen picture is the same four things. The job definition is the recipe card. The job is one dish from that card. The queue is the ticket rail. The compute environment is the kitchen, and it can open or close as demand changes.

How that scale to zero actually behaves is next.
