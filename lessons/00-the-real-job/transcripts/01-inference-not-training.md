# Video 01 — Inference, not training
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What it is.** **Training** updates model **weights** from many labeled examples — backpropagation, optimizers, epochs. **Inference** runs a **fixed** model on **new** inputs and returns outputs — here, a caption string per photo. This course is **inference-only**.

**Why the distinction drives architecture.** Training needs long GPU runs, checkpoint storage, experiment tracking, and often multi-node setups. Inference for vendor catalogs needs **repeatable jobs**, **clear inputs/outputs**, and **scale-to-zero** between drops — the AWS Batch shape.

**Example product story.** A restaurant group uploads ~30 dish photos to onboard a menu on a delivery app. The pipeline must return **one description per photo** for merchandisers to review — not retrain BLIP on their plates. The GPU runs the **same forward pass** many times; micro-batches of ~8 are memory management, not “eight separate products.”

**What we explicitly skip.** Fine-tuning, labeling workflows, hyperparameter search, distributed training loops.

**Visual:** Two paths — Training (weights change, weeks) vs Inference (weights frozen, minutes per folder) — highlight Inference for “food catalog.”

Why matrix math on images prefers GPUs — next.
