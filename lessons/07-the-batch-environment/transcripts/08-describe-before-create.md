# Video 08 — Describe before create
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

Describe tells you what this account already has. Create allocates something new, and a new compute environment is a new thing you can be billed for. Describe before create means you call describe with the name you expect. If the resource exists and it is healthy, you skip create and you reuse it. If describe comes back empty, the name is missing, and that is the only time you create it.

The three calls match the three objects. describe-compute-environments for the pool. describe-job-queues for the entrance. describe-job-definitions for the template. You read names, status, bindings, and revision numbers. Status VALID means Batch accepted the configuration. Status INVALID means stop. Read statusReason before you create anything else. A bad subnet, security group, instance profile, or service role shows up there. Creating a second environment with a new name does not repair the first one. It adds a pool beside a broken pool.

Cloud accounts are long-lived, and labs get rerun. A script that always creates a fresh name, my-ce-v2 and then my-ce-v3, leaves orphaned capacity paths. Each environment has its own maximum vCPUs. Each one can scale. The invoice then asks why one class has three GPU pools. The habit is the same one infrastructure tools use. You declare the desired name, you read current state, and you create only the gap. You do not create blindly at the start of every lecture.

Here is the lesson run twice. First time, describe on gpu-teaching-gpu-smoke-ce-spot returns empty. You create that Spot environment once. Managed, enabled, Spot, g4dn.xlarge, minimum vCPUs zero, maximum vCPUs four, image type ECS_AL2023_NVIDIA, instance profile ecsInstanceRole, and the subnet and security group from the course notes, subnet-b560b3fd and sg-bd00e4f5. You wait until status is VALID. That can take a minute or two. Only then do you create the queue gpu-teaching-gpu-smoke-queue-spot, enabled, priority one, order one bound to that environment. The job definition is the same idea. Describe active revisions of gpu-teaching-caption-job first. Register only when there is no active revision, or the image, the memory, the GPU, the role, or the logs are wrong. Register always mints a new revision, even when the JSON did not change.

Second time through the lesson, describe returns VALID. You reuse it, and you stop. You submit in lesson eight against the same names. No second Spot pool. The on-demand pair follows the same rule, gpu-teaching-gpu-smoke-ce-on-demand and gpu-teaching-gpu-smoke-queue-on-demand. Create each one only if its own describe says it is missing, and create the queue only after that environment is VALID.

The failure mode hides behind a zero. A duplicate environment with minimum vCPUs at zero looks idle, and it still scales up when jobs arrive. Two queues, two environments, two copies of the same submit, and the vCPU budget drains faster than the notes predicted. Reuse the gpu-teaching-gpu-smoke names. Do not invent a new suffix for practice.

On the screen, a flowchart with one entrance. Describe. If the name exists and status is VALID, reuse it. If the name is missing, create once, then describe again and wait for VALID. The INVALID branch leaves the chart and points at statusReason.

The next clip is that sequence on a real terminal. You will describe the Spot environment, the Spot queue, and the caption job, and you will create a piece only when the name is missing.
