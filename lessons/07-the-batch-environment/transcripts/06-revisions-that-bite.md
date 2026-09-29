# Video 06 — Job definition revisions
**Type:** Theory
**Runtime target:** ~3 minutes

---

Next up. Every register-job-definition on an existing name creates a new revision. AWS does not edit revision two in place. It appends the next number even if nothing changed. Submit with the bare name gpu-teaching-caption-job resolves to the latest active revision. Submit with a colon and a number pins that number. Pin when you mean to freeze a known good spec. Do not pin by accident because an old note says colon one.

Revisions give history and a way back. Latest is a moving pointer. A careless register moves it. Everyone who submits the bare name follows it.

This account has a real story. Revision one asks for sixteen thousand three hundred eighty-four mebibytes on a g4dn.xlarge. That cannot place. The job stays RUNNABLE with status reason MISCONFIGURATION:JOB_RESOURCE_REQUIREMENT. There are no app logs under /aws/batch/job, because logs appear only after STARTING or RUNNING. Revision one never gets there.

Revision two fixes the memory and leaves out jobRoleArn. Placement succeeds. CUDA can look fine. The first S3 call throws AccessDenied. You paid for the GPU minute to learn the role was empty.

Revision three and later is the usable pattern. Memory is twelve thousand two hundred eighty-eight mebibytes, and the job role is filled in. Revision four and later is the range you submit. Those keep that memory and role, and add explicit awslogs to /aws/batch/job. Do not submit colon one or colon two.

The common mistake is to fix a bad run by registering again without describe-job-definitions first. You can ship a new broken latest. Describe first. Read resourceRequirements, jobRoleArn, and logConfiguration. Register only when there is no active revision, or the image, memory, GPU, role, or logging is wrong. Every register creates another revision even when nothing changed. Write down the number that comes back.

A good revision still needs a queue. Next is how Spot and on-demand queues each bind to their own environment.
