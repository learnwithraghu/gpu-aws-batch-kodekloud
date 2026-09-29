# Video 06 — Logs as source of truth
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What they are.** Container **stdout/stderr** shipped to **CloudWatch Logs**, usually log group **`/aws/batch/job`**, one **log stream per job attempt**. The job record can include **`logStreamName`** for direct navigation.

**Why status alone is insufficient.** **`FAILED`** with exit code **1** is a headline: “something exited non-zero.” Causes include **`AccessDenied`** (job role), **`CUDA available: False`** (AMI/driver), **`ModuleNotFoundError`** (image drift), **empty photo list** (prefix mismatch), OOM killed by kernel.

**Example log snippets to show on screen (representative).** `AccessDenied` on **`GetObject`** → fix **`jobRoleArn`** or bucket policy. `Listed 0 keys` → fix **`IMAGE_PREFIX`** or upload path. `CUDA False` → CE AMI / GPU placement.

**Workflow.** **`describe-jobs`** → copy **`logStreamName`** → CloudWatch **Live tail** → fix lowest layer first (network, IAM, CUDA, then model).

**In this course.** Job definition revision **4+** should configure **awslogs** explicitly so streams exist when the container runs.

**Visual:** FAILED badge → magnifying glass on log line → fix category icon (IAM / prefix / CUDA).

Cancel and resubmit discipline — next.
