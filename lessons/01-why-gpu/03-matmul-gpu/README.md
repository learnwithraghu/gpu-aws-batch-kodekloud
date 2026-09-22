# Step 03 — Matmul on GPU

The same 2000×2000 multiply, but the tensors live in GPU memory.
This is the "aha" moment: same math, different device, very different time.

**Run:** `python main.py`

**Expected:** a few milliseconds (vs ~150 ms on CPU in step 02) — or, with no
local GPU, the recorded 8.2 ms from a g4dn.xlarge (NVIDIA T4).
