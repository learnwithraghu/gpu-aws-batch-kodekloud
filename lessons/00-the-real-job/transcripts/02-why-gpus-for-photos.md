# Video 02 — Why GPUs for captioning
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What it is.** Images become **large numeric tensors**. Vision-language models apply **layers of matrix operations** (convolutions, attention) to produce text tokens. **GPUs** execute many similar ops **in parallel**; **CPUs** excel at sequential, branching logic.

**Why it matters for a 30-photo folder.** A CPU **can** caption thirty images — eventually. A GPU finishes the folder in **one short batch job**, which matches “vendor waiting on catalog” SLAs and makes **minute-level GPU rental** economical vs hours of CPU time.

**Analogy.** One chef (CPU) plating every dish vs a line kitchen (GPU) with many hands doing the same step on different plates. Netflix encodes video frames with parallel hardware for the same reason — throughput on uniform math.

**Scope honesty.** This course is not claiming “AI requires GPU for everything.” It claims **this model + this batch size + this latency target** lands on a **T4** in Batch.

**Visual:** Grid of pixel numbers → tensor → parallel GPU cores → text caption.

Always-on GPU cost vs batch scale-to-zero — next.
