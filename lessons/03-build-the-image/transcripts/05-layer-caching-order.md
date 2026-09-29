# Video 05 — Layer caching
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What layer caching is.** Docker reuses unchanged layers from prior builds. Order: **base → pip → COPY code**.

**Why order matters.** Change **`describe_items.py`** → reuse pip layer, fast rebuild. Change **`requirements-gpu.txt`** → pip reruns, slow.

**Example timings.** First build **15–25 min**; code-only **minutes**.

**Visual:** Stack with “CACHED” labels on lower layers when only top changes.

Local tag vs ECR — next.
