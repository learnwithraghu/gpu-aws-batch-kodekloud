# Demo 007 — From Pixels to Tensors: Sequential CPU vs Parallel GPU

**Section:** 002 — GPU Fundamentals: From Silicon to Cloud
**Lecture#:** 007
**Sheet title:** [Demo] From Pixels to Tensors: Sequential CPU vs Parallel GPU
**Type:** Demo
**Runtime target:** ~6–8 minutes
**Topic code:** 002-007-[demo]-from-pixels-to-tensors-

---

## Teaching goal

Harden the Section 002 video ideas visually before Section 003 code. Using [`lessons/01-batch-and-gpu/gpu_cpu_simulator/`](../../lessons/01-batch-and-gpu/gpu_cpu_simulator/README.md), walk one KodeFood dish through four stages:

1. Photo → pixel grid → normalized tensor floats  
2. One shared multiply-and-add layer on every patch  
3. Sequential 4-core CPU vs parallel GPU waves (PCIe → VRAM)  
4. Scale from 1 photo to a vendor folder to marketplace volume  

## Before you record

```bash
cd lessons/01-batch-and-gpu/gpu_cpu_simulator
bash run_simulator.sh
# open http://127.0.0.1:8080
```

Confirm the header pill shows **`0 / 3 Checkpoints`**.

## Demo script (spoken flow)

1. **Stage 1 — What the computer sees.**  
   Point at the dish canvas. Toggle **Visual pixels** → **Raw RGB** → **Normalized floats**. Click one patch. Read `[R, G, B]` and `Shape: [3, H, W]` aloud. Tie it to the lecture line: *to a computer this is a grid of numbers, not noodles.*

2. **Stage 2 — Inside one layer.**  
   Click **Step 1 Block** and read the formula on screen. Click **Apply layer to all patches**. Emphasize: *same math on every cell — no branching — that is why GPUs fit this work.*

3. **Stage 3 — Sequential CPU vs parallel GPU.**  
   On **64 blocks**, click **Step** a few times on the CPU so Core 0–3 light up, then **Play**. Reset or leave CPU finished. Click **Run GPU**. Call out the PCIe line, then the two parallel waves. Read the compare bar (~× faster). Optionally switch to **256 blocks** and replay GPU only to show more work, still few waves.

4. **Stage 4 — Scale-up.**  
   Move the slider: **1 photo** → **30 photos** → **3,000 photos**. Contrast CPU backlog vs GPU burst. Close with Batch: *finite folder, short GPU burst, then scale toward zero.*

5. Confirm the green **`3 / 3 Checkpoints`** banner.

## What not to do in this demo

- Do not open `photos.py` / `describe_items.py` line-by-line (Section 003).  
- Do not create AWS Batch resources (Section 005).  
- Do not digress into VRAM micro-batch tuning as a separate mission — keep the story on pixels → tensors → parallelism.

## Checkpoint for students

Students should be able to say: *a dish becomes a tensor grid; every patch gets the same multiply-and-add; four CPU cores walk that grid sequentially while GPU SMs sweep it in parallel after PCIe into VRAM; at folder scale that gap becomes a systems reason to use Batch GPUs.*
