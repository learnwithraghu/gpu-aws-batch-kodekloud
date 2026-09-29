# Video 06 — Job definition revisions
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What it is.** Every time you call **`register-job-definition`** with a name that already exists, AWS creates a **new revision number** — `:1`, `:2`, `:3` — even if you only changed one field. **`submit-job`** with **`jobDefinition: gpu-teaching-caption-job`** (no suffix) resolves to the **latest active** revision unless you pin **`gpu-teaching-caption-job:4`**.

**Why it exists.** Operators need **history and rollback**. Production teams pin a known-good revision during a holiday freeze; dev teams iterate quickly. AWS never overwrites revision two in place — it appends revision three — so audits can answer “what spec did last Tuesday’s job use?”

**Example — teaching account story as cautionary labels.** **Revision 1:** memory **16384** MiB on `g4dn.xlarge` → **`MISCONFIGURATION:JOB_RESOURCE_REQUIREMENT`** → job never leaves **`RUNNABLE`**, no app logs. **Revision 2:** memory fixed but **no `jobRoleArn`** → placement succeeds → **`AccessDenied`** on S3. **Revision 3+:** **12288** MiB **and** job role **and** (in revision 4+) explicit **awslogs** → the pattern you want students on.

Show a timeline: three revision cards; only the last connects to **`SUCCEEDED`** and an S3 CSV.

**Common student mistake.** “Fixing” by registering again without **`describe-job-definitions`** — accidentally shipping a new broken latest, or leaving the class pinned to an old revision in notes while the console moved on.

**In this course.** Always **describe first**: read **`containerProperties`**, **`resourceRequirements`**, **`jobRoleArn`**, **`logConfiguration`**. Register intentionally; note the new revision number in your runbook.

**Visual:** Stack of revision cards; pointer “LATEST” on highest number; red stamps on :1 and :2.

How queues choose Spot vs on-demand hardware — next.
