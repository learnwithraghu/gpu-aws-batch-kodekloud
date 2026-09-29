# Video 05 — Job definition as contract
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What it is.** An AWS Batch **job definition** is a **registered template** that answers: “When Batch runs *this kind* of work, which container image should it use, how much CPU memory and GPU does it need, which IAM role does the *application inside the container* assume, and what command should start by default?” It is **not** a single run. It is the **spec** that many runs can share — like a job description posted on an internal careers site, not one employee’s first day on the job.

Batch stores definitions by **name** and **revision**. When you submit a job, you usually pass **`jobDefinition: my-name:revision`** or **`my-name`** and Batch picks the latest active revision. Think of revision numbers like versions of an API schema: consumers depend on the shape staying predictable.

**Why it exists.** Without a job definition, every submit call would have to repeat dozens of fields — image URI, resource limits, roles, logging — and operators would drift: one teammate asks for too much memory, another forgets the GPU flag, a third points at a test image. AWS centralizes that in a **versioned template** so platform teams can say “caption jobs always use *this* image, *this* GPU size, *this* S3 role,” while application teams only vary **per-run** inputs (which folder, which buckets) via **container overrides** in lesson eight.

**Example — read it like a form.** Picture a card on screen with these fields filled in for our course name **`gpu-teaching-caption-job`**:

- **Image:** an ECR URI such as `…/gpu-teaching:latest` — the program from lessons three and four.
- **vCPU:** four — we request the whole `g4dn.xlarge` vCPU count so placement matches one machine.
- **Memory:** twelve thousand two hundred eighty-eight mebibytes — not sixteen thousand; sixteen breaks placement on this instance type.
- **Resource requirements:** **`GPU` = 1** — tells the scheduler “only place me where a GPU is free.”
- **Job role ARN:** e.g. **`gpu-teaching-batch-job-role`** — S3 read/write for the catalog; without it, the container can start and still fail on the first photo download.
- **Command (default):** often a tiny CUDA check in lab setup — “does this image see a GPU?” — replaced at submit time by **`python /app/describe_items.py`** for real work.
- **Log configuration (good revisions):** send stdout to **`/aws/batch/job`** so lesson eight has a stream to open.

That card **is** the contract. Batch promises to **try** to run containers that honor it; your app promises to exit zero when the CSV is written.

**Overrides vs revisions — the decision students must memorize.** Change **which S3 prefix** or **which command** for *one* vendor folder → **container overrides** on `submit-job`, no new revision. Change **image URI**, **GPU count**, **memory**, or **job role for everyone** → register a **new job-definition revision**. Overrides cannot fix a broken template: if the definition still asks for sixteen gig memory or omits `jobRoleArn`, every run fails the same way.

**Visual for Remotion:** Left panel “Job definition (template)” with the field list above; right panel “Job (one run)” with job ID, status timeline, and a small “overrides” sticky on command + environment only. Animate an arrow from definition to many job icons labeled `describe-items-sample`, `describe-items-vendor-b`.

Revision numbers and how a bad “latest” hurts students — that is the next clip.
