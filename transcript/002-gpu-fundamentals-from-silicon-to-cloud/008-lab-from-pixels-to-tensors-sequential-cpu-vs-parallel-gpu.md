# Lab 008 — From Pixels to Tensors: Sequential CPU vs Parallel GPU

**Section:** 002 — GPU Fundamentals: From Silicon to Cloud
**Lecture#:** 008
**Sheet title:** [Lab] From Pixels to Tensors: Sequential CPU vs Parallel GPU
**Type:** Lab
**Runtime target:** ~15–20 minutes
**Topic code:** 002-008-[lab]-from-pixels-to-tensors--

---

## Lab goal

Complete the interactive **From Pixels to Tensors** lab in [`lessons/01-batch-and-gpu/gpu_cpu_simulator/`](../../lessons/01-batch-and-gpu/gpu_cpu_simulator/README.md) so you can see — not just hear — how a KodeFood dish photo becomes a tensor and why parallel GPUs beat sequential CPUs on that math.

## Prerequisites

- A modern web browser  
- This repository cloned locally  

## Steps

### 1. Launch the simulator

```bash
cd lessons/01-batch-and-gpu/gpu_cpu_simulator
bash run_simulator.sh
```

Open `http://127.0.0.1:8080` (or open `index.html` directly). Confirm **`0 / 3 Checkpoints`**.

### 2. Stage 1 — Inspect pixels as tensors

1. Toggle **Visual pixels**, **Raw RGB (0–255)**, and **Normalized floats (0–1)**.  
2. Optionally switch **8 × 8** vs **16 × 16**.  
3. Click at least one patch. Record its coordinates and the three raw + normalized channel values.  
4. Confirm checkpoint **1. Inspect pixel → tensor values** turns green.

### 3. Stage 2 — Step the shared layer formula

1. Click **Step 1 Block** and write down the printed multiply-and-add for that patch.  
2. Click **Apply layer to all patches** and watch the activation map fill.  
3. Answer for yourself: *why does “same formula on every patch” match GPU hardware?*

### 4. Stage 3 — Run CPU then GPU

1. Keep **64 blocks (1 photo)** first. Use **Step** at least twice on the CPU, then **Play** until finished.  
2. Click **Run GPU**. Watch **PCIe**, then parallel **SM** waves. Read the compare bar.  
3. Optional: switch to **256 blocks**, reset both, and run CPU Play + GPU again.  
4. Confirm checkpoints **2** and **3** are green and the lab completion banner appears.

### 5. Stage 4 — Scale the backlog

Move the slider through **1 photo**, **30 photos**, and **3,000 photos**. Note CPU vs GPU times at the vendor-folder setting (30).

## Deliverable

Screenshot or note the **`3 / 3 Checkpoints`** banner, plus one sentence each:

1. What does `Shape: [3, H, W]` mean for one dish photo?  
2. Why did the GPU finish the same grid in fewer ticks than the 4-core CPU?  
3. At 30 photos, why does a short GPU burst fit AWS Batch better than leaving a CPU backlog?

## Cleanup

If you started `run_simulator.sh`, press `Ctrl+C` to stop the local server.

## Common issues

| Symptom | Fix |
|---------|-----|
| Port `8080` in use | `PORT=8090 bash run_simulator.sh`, or open `index.html` directly |
| Checkpoint 1 still pending | Click a patch on the dish grid in Stage 1 |
| Checkpoints 2/3 pending | Finish a full CPU Play (or enough Steps to complete) and a full GPU Run |
