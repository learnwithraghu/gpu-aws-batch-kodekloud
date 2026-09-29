# Video 03 — Batch vs always-on GPU
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What it is.** **Always-on GPU** — an EC2 **`g4dn`** (or similar) running 24/7 whether or not work exists. **Batch scale-to-zero** — **`minvCpus: 0`**: instances appear when queued jobs need them and disappear when the queue is empty.

**Why food catalogs fit batch.** Uploads arrive in **bursts** — new vendor, seasonal menu, photo reshoot — not a steady stream every minute. Paying for idle GPU between bursts is like keeping a film render farm powered overnight for one scene that might arrive Tuesday.

**Example cost shape.** Flat spend line with **spikes** only during caption runs vs flat **high** line for reserved GPU. AWS Batch implements the spike pattern when CE minimum vCPUs is zero.

**When always-on wins.** Millisecond-latency APIs — fraud scoring on every click, voice assistants — need hot GPUs. Our workload has a **defined end** when the CSV lands.

**Visual:** Dollar chart — pulse vs flat high line; label Batch pulse “minvCpus=0”.

One folder in, one CSV out — the contract — next.
