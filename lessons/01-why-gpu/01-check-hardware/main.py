"""
Lesson 01 · Step 01 — check-hardware
What hardware does PyTorch see? No math yet — just look around.

Run:  python main.py
"""
import torch

print(f"PyTorch version : {torch.__version__}")
print(f"GPU available   : {torch.cuda.is_available()}")

if torch.cuda.is_available():
    props = torch.cuda.get_device_properties(0)
    print(f"GPU name        : {torch.cuda.get_device_name(0)}")
    print(f"GPU memory      : {props.total_memory / 1e9:.1f} GB")
else:
    print("No GPU here — that's fine. The next steps fall back to reference numbers.")
