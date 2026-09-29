# Video 08 — Describe before create
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What it is.** **`describe-*`** APIs (**`describe-compute-environments`**, **`describe-job-queues`**, **`describe-job-definitions`**) return **current state** — names, ARNs, status **`VALID`/`INVALID`**, bindings, revision numbers. **Create** APIs allocate **new** billable infrastructure. **Describe-before-create** means: call describe with the expected name; if the resource exists and is healthy, **skip create** and reuse.

**Why it exists.** Cloud accounts are long-lived. Labs rerun. Scripts that always create **`my-ce-v2`, `my-ce-v3`** leave **orphaned capacity paths** — each CE has its own **`maxvCpus`**, each can scale, and finance sees “why three GPU pools for one class?” Idempotent infra scripts match how Terraform plans: **desired state**, not “create blindly every lecture.”

**Example.** Instructor runs lesson seven twice. First run: describe returns empty → create Spot CE, queue, register job def. Second run: describe returns **`VALID`** → echo “reusing” → students submit jobs in lesson eight without duplicate CEs accidentally consuming Spot quota.

**Failure mode.** Duplicate CE with **`minvCpus=0`** still allows **scale-up** when jobs arrive — students double-submit across two queues tied to two CEs and wonder why quota drained faster.

**In this course.** Reuse **`gpu-teaching-gpu-smoke-*`** names from course docs. Create only when describe says the name is missing.

**Visual:** Flowchart — Describe → exists & VALID? → Yes: reuse / No: create once → describe again to confirm.

Demo next: the describe-or-create sequence on a real terminal.
