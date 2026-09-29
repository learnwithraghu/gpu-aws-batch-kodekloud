# Video 05 — Quotas and cold start
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**Service quotas — what they are.** Hard **account limits** on resource usage (here EC2 **G/VT vCPUs**). Batch CE **`VALID`** does **not** override quota. **`get-service-quota`** is ground truth.

**Spot vs on-demand codes.** Spot GPU requests: **`L-3819A6DF`**. On-demand G/VT running: **`L-DB2E81BA`** — need **≥ 4** for one **`g4dn.xlarge`**. Request increases via console or **`request-service-quota-increase`**; approval may take days.

**Cold start — what it is.** First job (or first after long idle) on a **new instance** pays: **EC2 boot**, **multi-GB ECR layer pull**, **Hugging Face weight download** into container FS. Two to five minutes before steady caption logs is **normal**, like the first DoorDash order waiting for a driver to reach a new zone.

**Warm instance** — subsequent job while instance still alive — skips boot and may skip full pull; still may download if image tag moved.

**Example narration.** Watch CloudWatch: silence → “Pulling” / agent lines → “Loading model” → batch progress. Do not cancel at 90 seconds if status is **`STARTING`**.

**Visual:** Timer stack — boot + pull + download + inference; second job with shorter stack.

Logs when status is FAILED — next.
