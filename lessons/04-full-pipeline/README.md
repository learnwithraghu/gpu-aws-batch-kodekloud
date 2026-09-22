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

## What the Scripts Do

`run_pipeline.py` (run locally):

1. Uploads the images in `assets/images/` to S3
2. Submits the `generate_captions` job (Lesson 03's script)
3. Submits the `verify_captions` job with `dependsOn` the first job
4. Polls both jobs until both reach a terminal state

Both jobs are submitted **instantly** — Batch handles the sequencing. Your
local script just waits.

`verify_captions.py` (runs in the container as Job 2):

1. Counts the images under the image prefix in S3
2. Downloads `captions/<batch-stem>/captions.csv` produced by Job 1
3. Checks every image has exactly one caption (fails the job otherwise)
4. Writes a `_VERIFIED` marker to S3 as proof the pipeline completed

Run it:

```bash
python run_pipeline.py
```

---

## Key Takeaway

> A pipeline is just submitted jobs with dependencies. Batch handles the
> "wait for step 1" part for you.  
> For larger pipelines, tools like AWS Step Functions or Airflow manage this
> graph, but the concept is identical.
