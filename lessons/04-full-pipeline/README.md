# Lesson 04 — The Full Pipeline

> **Concepts**: ML pipelines · Job dependencies (DAG) · AWS Batch `dependsOn`  
> **AWS needed**: Batch, S3

---

## What Is a Pipeline?

So far we've run each job manually, one at a time. In production, you want:

```
generate_captions  →  (only after success)  →  verify_captions
```

This is a **DAG** (Directed Acyclic Graph) — a sequence of steps where each
step depends on the previous one finishing successfully. If step 1 fails,
step 2 never runs.

AWS Batch has native support for this through `dependsOn`:

```python
job1 = batch.submit_job(...)

job2 = batch.submit_job(
    ...
    dependsOn=[{"jobId": job1["jobId"], "type": "N_TO_N"}]
)
```

Job 2 won't start until Job 1 reaches `SUCCEEDED`. If Job 1 fails, Job 2 is
automatically cancelled.

---

## The Steps

Three demos — break it, fix it, understand it:

| Step | You learn | Time |
|------|-----------|------|
| [01-two-jobs-no-order](01-two-jobs-no-order/) | Submit two jobs with NO ordering — watch verify fail | 15 min |
| [02-two-jobs-ordered](02-two-jobs-ordered/) | The same pipeline with `dependsOn` — it works | 15 min |
| [03-the-verify-job](03-the-verify-job/) | What the verify job checks (read it) | 5 min |

```bash
cd lessons/04-full-pipeline/01-two-jobs-no-order && python main.py
cd ../02-two-jobs-ordered && python main.py
```

---

## Key Takeaway

> A pipeline is just submitted jobs with dependencies. Batch handles the
> "wait for step 1" part for you.  
> For larger pipelines, tools like AWS Step Functions or Airflow manage this
> graph, but the concept is identical.
