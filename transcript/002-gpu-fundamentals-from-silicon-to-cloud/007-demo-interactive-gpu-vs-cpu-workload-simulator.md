# Demo 007 — Interactive GPU vs CPU Workload Simulator

**Section:** 002 — GPU Fundamentals: From Silicon to Cloud
**Lecture#:** 007
**Sheet title:** [Demo] Interactive GPU vs CPU Workload Simulator
**Type:** Demo
**Runtime target:** ~6–8 minutes
**Topic code:** 002-007-[demo]-interactive-gpu-vs-cpu-

---

## Teaching goal

Make the hardware concepts from Section 002 (`000`–`005`) visual and concrete before writing any Docker or PyTorch code in Section 003. Using the KodeFood Hardware Lab simulator in [`lessons/01-batch-and-gpu/gpu_cpu_simulator/`](../../lessons/01-batch-and-gpu/gpu_cpu_simulator/README.md), walk students through three interactive missions:

1. **Pixel & Tensor Race:** Why thousands of parallel GPU threads beat 4 fast CPU cores on uniform matrix math.
2. **CPU vs GPU Task Router:** Why the Host CPU still owns S3 downloads, JPEG decoding, and CSV creation while the GPU runs BLIP layers.
3. **Inside `g4dn.xlarge` (VRAM & Micro-Batch Tuner):** Why sending all 30 vendor photos at once triggers a CUDA Out-of-Memory (`OOM`) crash even when Host RAM is mostly free, and why `BATCH_SIZE=8` is the production sweet spot.

## Before you record

1. Start the local simulator (or open `index.html` directly in your browser):

```bash
cd lessons/01-batch-and-gpu/gpu_cpu_simulator
bash run_simulator.sh
# open http://127.0.0.1:8080
```

2. Confirm the top-right status pill reads **`0 / 3 Missions Complete`**.

## Demo script (spoken flow)

1. **Mission 1 — Pixel & Tensor Matrix Race.**
   - Point at the 64-block tensor grid representing one KodeFood dish photo.
   - Click **Run on CPU**. Watch 4 cores step through the grid 4 blocks at a time (`1,280 ms`).
   - Click **Run on GPU**. Watch parallel threads sweep the grid in two wide waves (`90 ms`).
   - State the takeaway: *CPU cores are built for sequential branching; GPU cores are built for uniform math across a grid.*
2. **Mission 2 — Route the KodeFood Pipeline.**
   - Click **Next: Mission 2**.
   - Deliberately route **1. List & Download Vendor Photos from Amazon S3** to **NVIDIA GPU + VRAM** first so students see the red diagnostic feedback explaining that GPUs have no network stack.
   - Route all 6 tasks to their proper side (`CPU` for S3 I/O, JPEG decode, keyword rule, and CSV upload; `GPU` for BLIP vision layers and token probabilities) until the counter hits **`6 / 6`**.
3. **Mission 3 — Tune Micro-Batching Without Crashing VRAM.**
   - Click **Next: Mission 3**. Point out the two separate 16.0 GB bars: **Host System RAM** and **NVIDIA T4 GDDR6 VRAM** connected by the **PCIe Bus**.
   - Select **`30 photos (All at once)`** and click **Run 30-Photo Vendor Folder**.
   - Highlight the red **`RuntimeError: CUDA out of memory!`** banner (`24.6 / 16.0 GB VRAM`) while Host RAM sits calmly at `5.4 / 16.0 GB`. Emphasize: *adding system RAM never fixes a GPU VRAM crash.*
   - Switch to **`8 photos (Default)`** with **Load BLIP weights once into VRAM** and run again. Point out the 4 micro-batch passes (`8 + 8 + 8 + 6`), `9.2 / 16.0 GB` VRAM usage, and `92%` GPU utilization.
   - Show the green **All 3 GPU Fundamentals Missions Complete!** banner at the top.

## What not to do in this demo

- Do not open `photos.py` or `describe_items.py` line-by-line yet — that is Section 003 Demo 002.
- Do not create AWS Batch resources yet — that is Section 005.

## Checkpoint for students

After this demo, students should be able to explain which KodeFood tasks stay on the CPU, which move to the GPU, and why `BATCH_SIZE=8` prevents a 16 GB T4 VRAM crash on `g4dn.xlarge`.
