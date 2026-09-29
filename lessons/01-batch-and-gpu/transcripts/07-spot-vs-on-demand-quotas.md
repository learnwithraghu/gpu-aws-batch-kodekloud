# Video 07 — Spot, on-demand, and the quota trap
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What they are.**

- **Spot instances** — Unused EC2 capacity sold at a discount; AWS can **interrupt** with notice when capacity is needed elsewhere.
- **On-demand instances** — Standard pay-by-the-second; **no reclaim** for capacity sharing in the same way.
- **Service quotas** — Account-level **limits** on how many vCPUs of a **family** you may run; **independent** of whether Batch CEs look healthy.

**Why this matters for GPU Batch.** **`g4dn`** is in the **G/VT** quota family. A queue bound to **on-demand** CE cannot launch if **on-demand G/VT quota is 0** — common on new accounts — even when the console shows CE **`VALID`**. Jobs sit **`RUNNABLE`** forever: **no instance, no logs**. Spot has a **different quota code** (**`L-3819A6DF`**); teaching accounts often have Spot headroom while on-demand G/VT is still zero.

**Example.** Team submits to on-demand queue after Spot slow; still **`RUNNABLE`**. They grep Python. Fix: **`get-service-quota`** for **`L-DB2E81BA`** (on-demand G/VT) — value **0** → request increase to **≥ 4** vCPUs → wait for approval → then on-demand fallback is real.

**In this course.** Default **Spot queue**; **`watch_batch_job.sh`** prints quota when **`RUNNABLE`** persists.

**Visual:** Two lanes Spot vs on-demand; red stop sign on on-demand lane labeled “quota = 0”.

Demo: run the quota CLI — next.
