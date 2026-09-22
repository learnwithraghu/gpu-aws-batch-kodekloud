# Lesson 02 — Your First AWS Batch GPU Job

> **Concepts**: AWS Batch · Compute Environment · Job Queue · Job Definition · CloudWatch Logs  
> **AWS needed**: Batch, ECR

---

## What is AWS Batch?

AWS Batch is a managed service that runs containerised jobs on EC2 instances — you submit a job, AWS picks an instance from your pool, runs your Docker container, and shuts the instance down when done.

Three concepts to know:

```
Compute Environment   →  the pool of EC2 instances (we use g4dn.xlarge Spot)
      ↓
Job Queue             →  where jobs wait until an instance is free
      ↓
Job Definition        →  the "template" for a job: which Docker image, how much CPU/GPU/RAM
      ↓
Job                   →  a single run: Job Definition + environment variables you pass at submit time
```

You don't manage instances. You don't SSH anywhere. You just submit a job and look at the logs.

---

## What the Job Does

`job.py` runs inside the container on the GPU:
1. Prints the GPU model name and memory
2. Creates two large random matrices on the GPU
3. Multiplies them
4. Prints how long it took

Simple — but it proves the GPU is working and accessible inside Batch.

---

## How to Run

Three short demos. Make sure the **one-time setup** in the root `README.md`
is done first — then it's the same habit every time: cd in, run.

| Step | You learn | Time |
|------|-----------|------|
| [01-the-container-script](01-the-container-script/) | The script Batch will run (read it) | 5 min |
| [02-submit-a-job](02-submit-a-job/) | Submit a job → get a job ID | 5 min |
| [03-watch-until-done](03-watch-until-done/) | Poll the job to SUCCEEDED | 10–15 min |

```bash
cd lessons/02-first-batch-job/02-submit-a-job && python main.py
cd ../03-watch-until-done && python main.py --job-id <id>
```

---

## Reading the Logs

After the job succeeds, go to:
`AWS Console → CloudWatch → Log Groups → /aws/batch/job`

You'll see something like:
```
GPU name   : NVIDIA Tesla T4
GPU memory : 15.7 GB
Matrix size: 5000 x 5000
Time       : 118.3 ms
Done.
```

---

## Key Takeaway

> Batch is just _"run this Docker container on a GPU instance, then stop."_  
> All the hard parts (finding an instance, pulling the image, terminating when done) are handled for you.
