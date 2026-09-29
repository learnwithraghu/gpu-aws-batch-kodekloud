# Video 01 — What AWS Batch is for
**Type:** Theory
**Runtime target:** ~3 minutes

---

Hello. Let's start with what AWS Batch actually is.

AWS Batch is a managed job scheduler for containerized work that has a start and an end. You register what a job looks like. That is the job definition. You register where it may run. That is a compute environment, plus a job queue. Then you submit individual jobs. Batch places those containers with ECS on EC2. It is not its own hypervisor. It is orchestration on top of EC2 capacity you configure. You submit the work. Batch places it when capacity exists.

It is not a notebook host, and it is not an interactive shell you keep open on the GPU. You do not SSH into a box to type Python. You define a job once, then submit many runs of that job.

It exists because teams run enormous numbers of finite tasks. Render a frame. Score a record. Convert a file. Caption a vendor folder of photos. Those tasks start, run to completion, and exit. They also peak at different times. Batch queues the work and scales the machines, so a GPU server is not left running while nobody is waiting, and so you are not launching an instance by hand for every job.

Set three AWS compute stories next to each other. An interactive notebook on EC2 is a human loop. You SSH in, or you open Jupyter, and one person iterates for hours. Lambda is a short burst. It fits an event handler that lasts seconds. It is a poor fit for downloading a ten gigabyte image and holding a T4 for eight minutes. Batch is the third story. You build a container once. You submit a job for one vendor folder, and another job for the next. Each run is tracked, retried, and logged on its own.

In this course, one job is about one vendor folder, and that folder becomes one CSV with accepted and rejected rows. You read CloudWatch, and you read S3, to see what happened. The definition stays. Two folders are two submits, two job IDs, two logs. If the second fails, you retry that job. You do not reopen a notebook and hope you remember which cell worked.

Every Batch diagram uses four nouns. A compute environment, a queue, a job definition, and a job. Those four, with a kitchen picture that keeps them apart, are next.
