# Step 01 — Cost math

The cost model with zero AWS calls: spot price × minutes × number of batches.
Wall-clock stays flat (parallel array jobs) while cost grows linearly.

**Run:** `python main.py`

**Expected:** a small table — 1 batch ≈ $0.0033, 100 batches ≈ $0.33, all in
about the same wall-clock time.

Change `SPOT_PRICE_PER_HOUR` or `CAPTION_MINUTES` and re-run to explore.
