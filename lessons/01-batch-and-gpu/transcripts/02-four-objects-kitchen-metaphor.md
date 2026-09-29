# Video 02 — The four Batch objects
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

Four objects show up on every Batch diagram, and this course has a real name for each of them.

The compute environment is the rule for which EC2 capacity Batch may start. Instance types. Spot or on demand. The network. Minimum and maximum vCPUs. The machine image, when the job needs a GPU. The Spot environment here is gpu-teaching-gpu-smoke-ce-spot. In a sentence, it may use a Spot g4dn.xlarge in Tokyo, region ap-northeast-1, and it may scale from zero.

The job queue is the line jobs enter when you submit them. A queue does not hold servers. It holds jobs. It is bound to one or more compute environments, with a priority. This course uses gpu-teaching-gpu-smoke-queue-spot, and that queue uses the Spot environment. When a job is waiting, the environment can start an instance. When the queue is empty, minimum vCPUs of zero lets capacity fall away. You pay for the instance only while it is up.

The job definition is a registered template, versioned, and it is not one run. It records the ECR image, CPU, memory, GPU, the job role for calls the container makes, the default command, and logging. AWS stores it as a name and a revision. You will see that pair written like caption-job, colon, four. Submit usually passes the name, and Batch picks the latest active revision unless you pin one. Our template is gpu-teaching-caption-job. Read it as, run gpu-teaching, colon, latest, one GPU, twelve gibibytes of memory, a job role that can touch S3, and a default command that checks CUDA. Use the highest active revision. Revision one asks for sixteen thousand three hundred eighty-four mebibytes. Revision two has no job role. Revision three and later are the ones that place and can write the CSV.

The job is one execution of that template. It has its own job ID, a status timeline from SUBMITTED through to SUCCEEDED, and optional overrides that apply to this run only. Tonight's job is the prefix images/sample, with overrides that point describe_items.py at that folder.

The split exists so ownership stays clear. Platform teams own compute environments and queues. That is cost, security, and instance types. Application teams own job definitions and submits. That is business logic and environment variables. A job is also the unit finance can audit. The question, what did vendor X cost, is answered per job ID, not against a vague cluster.

Changing the Docker image for everyone means a new job definition revision. Changing only this folder's S3 prefix means a submit override. It does not mean a new revision. And three names from older examples are not resources in this account. gpu-teaching-ce, gpu-teaching-queue, and gpu-teaching-job-def. Do not create them.

The kitchen picture is the same four things. The job definition is the recipe card in the back office. The job is one burrito made from that card. The queue is the ticket rail when the grills are busy. The compute environment is the kitchen, and it can open or close grill lines as demand changes.

On the screen, four boxes run left to right. One definition card throws off a job icon, and the same card can throw off many jobs.

The kitchen can close because minimum vCPUs can be zero. How that scale to zero actually behaves is next.
