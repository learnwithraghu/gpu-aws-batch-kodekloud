# Video 06 — Inference mode, not training
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What it is.** **`model.eval()`** — inference behavior for layers like dropout/batchnorm. **`torch.no_grad()`** — disable autograd graph for forward-only passes.

**Why use both in caption jobs.** Training builds graphs for **backward** passes; inference does not need them — saves **memory and time**. Matches frozen BLIP weights — no optimizer step.

**Example anti-pattern.** Training mode on inference can change dropout randomness and inflate memory — wrong for production catalog generation.

**Visual:** Cross out backward arrow; highlight forward-only path to text tokens.

BLIP prompt and **`generate`** args — next.
