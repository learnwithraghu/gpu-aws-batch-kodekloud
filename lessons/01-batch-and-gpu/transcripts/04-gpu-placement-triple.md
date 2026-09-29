# Video 04 — The GPU placement triple
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What it is.** **Placement** is Batch’s decision: “which EC2 instance, if any, satisfies this job’s resource request?” For GPU jobs, three independent settings must **align** or the job never reaches **`RUNNING`**.

**Why it exists.** GPUs are **scarce, specialized resources**. The scheduler must match **host capabilities** (driver, device), **job requests** (GPU count, memory), and **CE constraints** (allowed instance types). One wrong field blocks placement — often with **no application logs** because the container never started.

**The triple — teach with three padlocks on one door.**

1. **Host AMI / image type** — **`ECS_AL2023_NVIDIA`** (or equivalent): NVIDIA drivers + ECS GPU support. Plain Linux on `g4dn` → GPU invisible inside container.
2. **Job definition GPU requirement** — **`resourceRequirements: [{ type: GPU, value: "1" }]`** — scheduler will not place on CPU-only shapes.
3. **Memory request ≤ usable RAM on instance** — `g4dn.xlarge` advertises 16 GiB; ECS reserves overhead. **16384 MiB** often yields **`MISCONFIGURATION:JOB_RESOURCE_REQUIREMENT`** — stuck **`RUNNABLE`**. Course uses **12288 MiB**.

**Example error story.** Student sees **`RUNNABLE`** for twenty minutes, opens CloudWatch — **empty**. They edit Python. Fix: **`describe-job-definitions`**, lower memory, confirm GPU and CE instance type include **`g4dn.xlarge`**.

**Visual:** Door labeled “RUNNING”; three locks AMI / GPU=1 / memory; red job stuck at RUNNABLE when one lock open.

Why one whole `g4dn` per catalog job — next.
