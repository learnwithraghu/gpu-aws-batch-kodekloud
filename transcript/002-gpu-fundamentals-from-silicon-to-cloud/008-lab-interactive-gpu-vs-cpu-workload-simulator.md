# Lab 008 — Interactive GPU vs CPU Workload Simulator

**Section:** 002 — GPU Fundamentals: From Silicon to Cloud
**Lecture#:** 008
**Sheet title:** [Lab] Interactive GPU vs CPU Workload Simulator
**Type:** Lab
**Runtime target:** ~15–20 minutes
**Topic code:** 002-008-[lab]-interactive-gpu-vs-cpu-w

---

## Lab goal

Run the interactive **KodeFood Hardware Lab** simulator in [`lessons/01-batch-and-gpu/gpu_cpu_simulator/`](../../lessons/01-batch-and-gpu/gpu_cpu_simulator/README.md) and complete all three hands-on missions to verify how CPU cores, GPU cores, PCIe transfers, and VRAM micro-batching behave on a `g4dn.xlarge` workload.

## Prerequisites

- A modern web browser
- This repository cloned locally (or on your lab workstation)

## Steps

### 1. Launch the Simulator

From the repository root, start the simulator server (or open `index.html` directly in your browser):

```bash
cd lessons/01-batch-and-gpu/gpu_cpu_simulator
bash run_simulator.sh
```

Open `http://127.0.0.1:8080` in your browser. Confirm the header pill shows **`0 / 3 Missions Complete`**.

### 2. Complete Mission 1 — Pixel & Tensor Race

1. In **Mission 1**, click **Run on CPU** and observe how 4 sequential cores step through the 64 image tensor blocks.
2. Click **Run on GPU** and observe how parallel threads process the same 64 blocks in wide waves.
3. Confirm the **Mission 1** tab status badge turns green (**`Complete`**), then click **Next: Mission 2 →**.

### 3. Complete Mission 2 — CPU vs GPU Task Router

1. For each of the 6 KodeFood pipeline operations, choose either **Host CPU + RAM** or **NVIDIA GPU + VRAM**:
   - Listing & downloading S3 objects (`photos.py`)
   - Decoding JPEG/PNG files & checking file extensions
   - Running BLIP vision transformer layers (`describe_items.py`)
   - Computing caption token probabilities
   - Applying the `accepted` vs `rejected` food keyword rule
   - Formatting and uploading `descriptions.csv` to S3
2. Read the diagnostic explanation under each row until your score reaches **`6 / 6`** and the **Mission 2** tab badge turns **`Complete`**.
3. Click **Next: Mission 3 →**.

### 4. Complete Mission 3 — Inside `g4dn.xlarge`: VRAM & Micro-Batch Tuner

1. Select **`30 photos (All at once)`** under `BATCH_SIZE` and click **Run 30-Photo Vendor Folder on `g4dn.xlarge`**.
2. Observe the **`RuntimeError: CUDA out of memory!`** failure (`24.6 / 16.0 GB` VRAM) and note the Host System RAM usage (`5.4 / 16.0 GB`).
3. Next, test **`1 photo`** and **`8 photos (Default)`**, and compare **Load BLIP weights once into VRAM** vs **Reload weights over PCIe every batch**.
4. Run **`8 photos (Default)`** with **Load BLIP weights once into VRAM** to complete the second checkpoint (`9.2 / 16.0 GB` VRAM, `92%` GPU utilization).
5. Confirm the top banner appears: **`All 3 GPU Fundamentals Missions Complete!`**

## Deliverable

Record or screenshot the completed **`3 / 3 Missions Complete`** banner and answer in one sentence each:

1. Why does downloading S3 files slowly on a GPU instance waste money?
2. Why did `BATCH_SIZE=30` crash with a CUDA out-of-memory error even though over 10 GB of Host System RAM was still free?

## Cleanup

If you started `run_simulator.sh`, press `Ctrl+C` in the terminal to stop the local HTTP server.

## Common issues

| Symptom | Fix |
|---------|-----|
| Port `8080` is already in use | Run with a custom port: `PORT=8090 bash run_simulator.sh`, or open `index.html` directly in your browser |
| Mission 3 badge still says `Pending` | Make sure you ran both `BATCH_SIZE=30` (to observe the OOM crash) and `BATCH_SIZE=8` with weights loaded once |
