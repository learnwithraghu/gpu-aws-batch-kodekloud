# Lesson 06 — The Full Pipeline

> **Concepts**: ML pipelines · Job dependencies (DAG) · AWS Batch `dependsOn`  
> **AWS needed**: Batch, S3

---

## What Is a Pipeline?

So far we've run each job manually, one at a time. In production, you want:

```
extract_frames  →  (only after success)  →  embed_frames
```

This is a **DAG** (Directed Acyclic Graph) — a sequence of steps where each step depends on the previous one finishing successfully. If step 1 fails, step 2 never runs.

AWS Batch has native support for this through `dependsOn`:

```python
job1 = batch.submit_job(...)

job2 = batch.submit_job(
    ...
    dependsOn=[{"jobId": job1["jobId"], "type": "N_TO_N"}]
)
```

Job 2 won't start until Job 1 reaches `SUCCEEDED`. If Job 1 fails, Job 2 is automatically cancelled.

---

## What `run_pipeline.py` Does

1. Submits the `extract_frames` job (Lesson 03's logic)
2. Submits the `embed_frames` job (Lesson 04's logic) with `dependsOn` the first job
3. Polls both jobs until both reach a terminal state
4. Prints where to find the final embeddings in S3

Both jobs are submitted **instantly** — Batch handles the sequencing. Your local script just waits.

---

## Key Takeaway

> A pipeline is just submitted jobs with dependencies. Batch handles the "wait for step 1" part for you.  
> For larger pipelines, tools like AWS Step Functions or Airflow manage this graph, but the concept is identical.
