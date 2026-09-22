# Step 02 — Submit a job

One API call: `submit_job`. You get a job ID back and that's it — no SSH,
no instance management.

**Run:** `python main.py`

**Expected:** a line like `Submitted job : 8f3c…` plus the exact command to
watch it (step 03). The job runs `job.py` from step 01 on a g4dn.xlarge.
