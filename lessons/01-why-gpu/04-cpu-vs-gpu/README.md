# Step 04 — CPU vs GPU benchmark

The full comparison across 500², 2000², and 5000² matrices, with a speedup
column. This is the payoff of the whole lesson.

**Run:** `python main.py`

**Expected:**

```
      size |  CPU (ms) |  GPU (ms) |  speedup
--------------------------------------------------
   500x500 |       4.2 |       0.8 |     5.3x
  2000x2000|     145.7 |       8.2 |    17.8x
  5000x5000|    3612.4 |     119.0 |    30.4x
```

GPUs pay off at scale — exactly why we caption whole batches on GPU.
