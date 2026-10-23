# Demo 007 — Sequential CPU vs Parallel GPU

**Section:** 002 — GPU Fundamentals: From Silicon to Cloud
**Lecture#:** 007
**Sheet title:** [Demo] Sequential CPU vs Parallel GPU
**Type:** Demo
**Runtime target:** ~4–6 minutes
**Topic code:** 002-007-[demo]-sequential-cpu-vs-parall

---

## Teaching goal

Make one idea visual and sticky: **the same dish tensor and the same math finish much faster on a GPU because work runs in parallel waves, not a long sequential march of CPU cores.**

Use [`lessons/01-batch-and-gpu/gpu_cpu_simulator/`](../../lessons/01-batch-and-gpu/gpu_cpu_simulator/README.md).

## Before you record

```bash
cd lessons/01-batch-and-gpu/gpu_cpu_simulator
bash run_simulator.sh
# open http://127.0.0.1:8080
```

## Demo script (spoken flow)

1. **Frame the page.** Same KodeFood dish tensor on both sides. Same multiply-and-add on every block. Only the hardware style changes.
2. **CPU side.** Click **Step** a few times so Core 0–3 light up and only four blocks advance per tick. Then **Play CPU**. Call out ticks, blocks done, and time.
3. **GPU side.** Click **Play GPU**. Watch wide parallel waves finish the same grid in far fewer steps.
4. **Read the compare bar.** CPU time vs GPU time and the × factor. One sentence takeaway: *sequential cores vs parallel waves — that is why caption math prefers a GPU.*
5. **Optional.** Switch to **256 blocks**, Reset, and replay once to show the gap still holds on a larger grid.

## What not to do in this demo

- Do not open application source code yet (Section 003).
- Do not create Batch resources yet (Section 005).
- Do not add extra missions (VRAM tuner, task routing, scale slider) — keep this demo to the side-by-side race only.

## Checkpoint for students

Students should be able to say: *four CPU cores walk the tensor block by block; a GPU sweeps many blocks per wave; same math, different parallelism.*
