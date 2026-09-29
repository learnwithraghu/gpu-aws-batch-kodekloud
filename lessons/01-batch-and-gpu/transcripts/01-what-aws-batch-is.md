# Video 01 — What AWS Batch is for
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

AWS Batch is a managed job scheduler for containerized work that has a start and an end. You register what a job looks like. That is the job definition. You register where it may run. That is a compute environment, plus a job queue. Then you submit individual jobs. Batch places those containers with ECS on EC2. It is not its own hypervisor. It is orchestration on top of EC2 capacity you configure. You submit the work. Batch places it when capacity exists. It is not a notebook host, and it is not an interactive shell you keep open on the GPU.

It exists because data and machine learning teams run enormous numbers of finite tasks. Render a frame. Score a record. Convert a file. Caption a folder of photos. Those tasks share a pattern. They start, they run to completion, and they exit. They also peak at different times. Batch queues the work and scales the machines, so a GPU server is not left running while a person sleeps, and so you are not SSHing in to launch an instance by hand for every job the way teams did in two thousand five.

Set three AWS compute stories next to each other. An interactive notebook on EC2 is a human loop. You SSH in, or you open Jupyter, and one person iterates for hours. Lambda is a short burst. It fits an event handler that lasts seconds. It is a poor fit for downloading a ten gigabyte image and holding a T4 for eight minutes. Batch is the third story. You build a container once. You submit a job, job ID abc, for vendor A, and another job, job ID def, for vendor B. Each run is tracked, retried, and logged on its own. That is how a large nightly pipeline thinks about work, and how a visual effects render farm thinks about it. Procter and Gamble style batches, and render farms, are both piles of finite units.

In this course, one job is about one vendor folder, and that folder becomes one CSV. You do not SSH into the GPU box to type Python. You read CloudWatch, and you read S3, to see what happened. This course's work, photos in and a CSV out, fits a job you define once and submit many times. The definition stays. Vendor A's run and vendor B's run are two submits, two job IDs, two logs. If vendor B fails, you retry that job. You do not reopen a notebook and hope you remember which cell worked.

On the screen, three columns sit side by side. A notebook, with a human in the loop. Lambda, a short burst. Batch, a container queue that scales. The catalog job sits under Batch.

Every Batch diagram uses four nouns. A compute environment, a queue, a job definition, and a job. Those four, with a kitchen picture that keeps them apart, are next.
