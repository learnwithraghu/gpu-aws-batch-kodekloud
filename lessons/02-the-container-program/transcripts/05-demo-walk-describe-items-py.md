# Video 05 — Demo: walk through describe_items.py
**Type:** Demo  
**Runtime target:** ~3–4 minutes

---

**Purpose.** Connect **model code** to **I/O module** — the full worker Batch schedules.

Open **`describe_items.py`**. Show import from **`photos.py`**. **`main`**: list work → chunk into **`BATCH_SIZE`** groups (e.g. 8+8+8+6 for 30 photos) → load BLIP → **`generate`** with prefix → collect text → **`save_csv`** after **all** groups succeed.

Narrate **first cloud run** may download weights from Hugging Face — network + disk, not in this local read.

**Visual:** Loop diagram over batches; single CSV at end.

Inference mode (`eval`, `no_grad`) — next theory.
