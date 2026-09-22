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

1. Make sure you've completed the **one-time setup** in the root `README.md`
2. Run the submit script from this folder:

```bash
python submit_job.py
```

The script:
- Submits `job.py` to AWS Batch
- Polls every 10 seconds until it finishes
- Prints the job ID and final status

To find the job's log stream, go to:
`AWS Console → CloudWatch → Log Groups → /aws/batch/job`

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
