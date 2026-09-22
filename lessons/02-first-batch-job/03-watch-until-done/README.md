# Step 03 — Watch until done

Poll the job every 10 seconds. Statuses walk
`SUBMITTED → RUNNABLE → STARTING → RUNNING → SUCCEEDED`.

**Run:** `python main.py --job-id <id from step 02>`

**Expected:** the status lines, then `✅ Job SUCCEEDED` and where to find the
CloudWatch logs (GPU name, memory, matmul time).
