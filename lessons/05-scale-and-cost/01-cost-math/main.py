"""
Lesson 05 · Step 01 — cost-math
What does GPU captioning actually cost? No AWS — just arithmetic you can
change and re-run.

Run:  python main.py
"""
# Approximate numbers for g4dn.xlarge (NVIDIA T4) Spot in ap-northeast-1
SPOT_PRICE_PER_HOUR = 0.20   # USD — typical range $0.16–0.24
CAPTION_MINUTES     = 1.0    # per image batch (load model + caption ~20 images)

cost_per_batch = SPOT_PRICE_PER_HOUR * CAPTION_MINUTES / 60

print(f"Spot price     : ${SPOT_PRICE_PER_HOUR:.2f}/hr")
print(f"Time per batch : {CAPTION_MINUTES:.1f} min")
print(f"Cost per batch : ${cost_per_batch:.4f}\n")

print(f"{'batches':>8} | {'wall-clock':>10} | {'total cost':>10}")
print("-" * 36)
for n in [1, 5, 10, 50, 100]:
    # Array job: all batches run in PARALLEL → wall-clock stays ~1 batch
    wall_clock = CAPTION_MINUTES
    total_cost = cost_per_batch * n
    print(f"{n:>8} | {wall_clock:>9.0f} m | ${total_cost:>9.4f}")

print()
print("Parallel array jobs: wall-clock time stays flat, cost grows linearly.")
print("Rule of thumb: neural network + >1000 items → GPU is worth it.")
