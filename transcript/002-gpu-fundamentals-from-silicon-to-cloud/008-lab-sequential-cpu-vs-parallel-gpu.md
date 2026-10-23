# Lab 008 — Sequential CPU vs Parallel GPU

**Section:** 002 — GPU Fundamentals: From Silicon to Cloud
**Lecture#:** 008
**Sheet title:** [Lab] Sequential CPU vs Parallel GPU
**Type:** Lab
**Runtime target:** ~10–15 minutes
**Topic code:** 002-008-[lab]-sequential-cpu-vs-paralle

---

## Lab goal

Run the interactive **Sequential CPU vs Parallel GPU** lab and compare how the same KodeFood dish tensor finishes on both sides.

App: [`lessons/01-batch-and-gpu/gpu_cpu_simulator/`](../../lessons/01-batch-and-gpu/gpu_cpu_simulator/README.md)

## Prerequisites

- A modern web browser
- This repository cloned locally

## Steps

### 1. Launch

```bash
cd lessons/01-batch-and-gpu/gpu_cpu_simulator
bash run_simulator.sh
```

Open `http://127.0.0.1:8080` (or open `index.html` directly).

### 2. Run the CPU side

1. Keep **64 blocks**.
2. Click **Step** at least twice and watch Core 0–3 advance four blocks per tick.
3. Click **Play CPU** and wait until it finishes. Note the tick count and time.

### 3. Run the GPU side

1. Click **Play GPU**.
2. Watch the parallel waves fill the grid.
3. Note the wave count and time.

### 4. Read the comparison

Confirm the green compare bar shows CPU time vs GPU time and the × factor.

### 5. Optional larger grid

Switch to **256 blocks**, click **Reset**, run **Play CPU** and **Play GPU** again, and note whether the GPU still finishes in fewer steps.

## Deliverable

Screenshot or note the comparison bar, plus one sentence:

> Why did the GPU finish the same grid faster than the 4-core CPU?

## Cleanup

If you started `run_simulator.sh`, press `Ctrl+C` to stop the server.

## Common issues

| Symptom | Fix |
|---------|-----|
| Port `8080` in use | `PORT=8090 bash run_simulator.sh`, or open `index.html` directly |
| Compare bar still waiting | Finish both **Play CPU** and **Play GPU** on the same grid size |
