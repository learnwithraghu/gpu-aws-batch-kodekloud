# Video 04 — S3 size vs GPU memory
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What happens to bytes.** Download JPEG (small) → decode to RGB tensor (large) → batch on GPU (larger still).

**Why BATCH_SIZE counts photos.** Memory bound by **decoded batches**, not S3 megabyte sum.

**Example.** 8 × 12MP images can OOM where 8 × 2MP succeeds — tune batch or resize in future work.

**Visual:** JPEG icon expands to tensor block in GPU.

Don't rebuild for new photos — sync is data-only.

Demo sync — next.
