# Video 06 — Job definition revisions
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

Every call to register-job-definition on a name that already exists creates a new revision. Revision one, then two, then three, and so on. AWS does not edit revision two in place. It appends the next number, even if you changed a single field, and even if you changed nothing. Submit with the bare name gpu-teaching-caption-job resolves to the latest active revision. Submit with gpu-teaching-caption-job, colon, and a number, pins that number. You pin when you mean to freeze a known good spec. You do not pin by accident because an old note still says colon one.

Revisions exist so there is history and a way back. A production team can pin a known good revision during a freeze. A lab can iterate. An audit can answer what spec last Tuesday's job used, because the revision on that job is still stored. The cost of that history is that latest is a moving pointer. A careless register moves the pointer. Everyone who submits the bare name follows it.

This account has a real story, and it is the cautionary label on the early numbers. Revision one asks for sixteen thousand three hundred eighty-four mebibytes on a g4dn.xlarge. That instance type cannot place it. The job stays RUNNABLE. The status reason is MISCONFIGURATION, colon, JOB_RESOURCE_REQUIREMENT. The application never starts, so there are no app logs under slash aws slash batch slash job. Logs show up only after STARTING or RUNNING. Revision one never gets there.

Revision two fixes the memory and leaves out jobRoleArn. Placement succeeds. The container starts. CUDA can look fine. The first S3 call throws AccessDenied. You paid for the GPU minute to learn that the role was empty.

Revision three and later is the usable pattern. Memory is twelve thousand two hundred eighty-eight mebibytes, and the job role is filled in, so the job can place and can write the CSV. Revision four and later is the range you submit. Those revisions keep that memory and that role, and they add an explicit awslogs configuration to the group slash aws slash batch slash job. When the source of truth is the highest active revision, four and up is the good range. Do not submit colon one or colon two.

The common mistake is to fix a bad run by registering again, without describe-job-definitions first. You can ship a new broken latest, or you can leave the class notes pinned to an old revision while the console has moved on. Describe first. Read containerProperties. Read resourceRequirements, the memory and the GPU. Read jobRoleArn. Read logConfiguration. Register only when there is no active revision, or the image, the memory, the GPU, the role, or the logging config is wrong. Every register creates another revision even when nothing changed, so you do not register just to feel sure. Write down the revision number that comes back.

On the screen, a stack of revision cards. A pointer labeled latest sits on the highest number. Revision one and revision two carry a red stamp. Only the latest good card connects to a succeeded job and an S3 CSV.

A good revision still does nothing until a queue will run it. The next clip is how the Spot queue and the on-demand queue each bind to their own compute environment.
