# Video 08 — Describe before create
**Type:** Theory
**Runtime target:** ~3 minutes

---

Alright. Describe tells you what this account already has. Create allocates something new, and a new compute environment is a new thing you can be billed for. Call describe with the name you expect. If it exists and is healthy, reuse it. If describe comes back empty, the name is missing, and that is the only time you create.

The three calls match the three objects. describe-compute-environments for the pool. describe-job-queues for the entrance. describe-job-definitions for the template. Status VALID means Batch accepted the config. INVALID means stop. Read statusReason before you create anything else. A bad subnet, security group, instance profile, or service role shows up there. A second environment with a new name does not repair the first. It adds a pool beside a broken pool.

Labs get rerun. A script that always creates my-ce-v2 then my-ce-v3 leaves orphaned capacity paths. Each environment has its own max vCPUs and can scale. The invoice then asks why one class has three GPU pools. Declare the desired name, read current state, create only the gap.

First time through, describe on gpu-teaching-gpu-smoke-ce-spot returns empty. Create that Spot environment once. Managed, enabled, Spot, g4dn.xlarge, min zero, max four, image type ECS_AL2023_NVIDIA, instance profile ecsInstanceRole, subnet subnet-b560b3fd, security group sg-bd00e4f5. Wait until VALID. Then create queue gpu-teaching-gpu-smoke-queue-spot, enabled, priority one, bound to that environment. For the job definition, describe active revisions of gpu-teaching-caption-job first. Register only when there is no active revision, or the image, memory, GPU, role, or logs are wrong. Register always mints a new revision.

Second time, describe returns VALID. Reuse it and stop. Submit in lesson eight against the same names. The on-demand pair follows the same rule. Create each only if its own describe says missing, and create the queue only after that environment is VALID.

A duplicate environment with min vCPUs at zero looks idle and still scales when jobs arrive. Reuse the gpu-teaching-gpu-smoke names. KodeFood's shared GPU pool is one pool, not a new name every lecture.

Next clip runs that sequence on a real terminal.
