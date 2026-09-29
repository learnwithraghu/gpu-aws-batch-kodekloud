# Video 05 — g4dn and the T4 in practice
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What it is.** **`g4dn.xlarge`** is an EC2 **instance type**: one **NVIDIA T4** GPU, **4 vCPUs**, **16 GiB** host memory, general-purpose network. It sits in AWS’s “small GPU inference” tier — cheaper than **`p4`** training monsters, enough for vision-language models on small batches.

**Why it exists in catalog workloads.** Food photo captioning with BLIP is **throughput-over-time**, not trillion-parameter training. A T4 running micro-batches of ~8 images finishes a ~30-photo folder in one job without provisioning **`p3`** hardware you cannot fill.

**Example — resource ask.** Job definition requests **4 vCPU, 12288 MiB, 1 GPU** → Batch places **one job on one whole instance** in this course. We do **not** bin-pack four separate one-GPU jobs onto one `g4dn` — that optimization belongs to large internal schedulers at Meta, not this teaching pipeline. One folder, one job, one machine, one CSV simplifies debugging and IAM.

**Contrast for advanced students.** Kubernetes with fractional GPUs or multi-GPU sharing is a different lesson; Batch here is **whole-instance placement** via ECS.

**Visual:** Single container occupying full instance box; T4 chip icon; 30 photos → one CSV arrow out.

Two IAM roles — host vs container — next.
