# Step 01 — Two jobs, no order (the bug)

Submit the caption job and the verify job at the same time — nothing ties
them together. The verify job starts immediately, finds no
`captions/<stem>/captions.csv`, and **fails**.

**Run:** `python main.py [--batch-stem pipeline-demo]`

**Expected:** `Job 2 (verify): ❌ FAILED` while the caption job is still
running — a data race. This is why pipelines need dependencies.

(If verify happens to finish after captioning by luck, re-run with a fresh
`--batch-stem` to see the failure.)
