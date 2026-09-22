# Step 02 — Two jobs, ordered (the fix)

Identical to step 01 except for **one line**:

```python
dependsOn=[{"jobId": job1_id, "type": "N_TO_N"}]
```

Job 2 now sits in `PENDING` until Job 1 reaches `SUCCEEDED`. If Job 1 fails,
Job 2 is cancelled — you never verify captions that were never made.

**Run:** `python main.py [--batch-stem pipeline-demo]`

**Expected:** `Job 2 (verify)` stays `PENDING` while Job 1 runs, then
`✅ Job 2 (verify): SUCCEEDED`, plus the caption file and `_VERIFIED` marker.
