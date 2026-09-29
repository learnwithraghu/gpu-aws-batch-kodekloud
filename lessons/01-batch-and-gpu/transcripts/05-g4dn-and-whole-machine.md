# Video 05 — g4dn and the T4 in practice
**Type:** Theory
**Runtime target:** ~3 minutes

---

Next up. The machine this course actually buys.

g4dn.xlarge is an EC2 instance type. It gives you one NVIDIA T4, four vCPUs, sixteen gibibytes of host memory, and general purpose networking. It sits in AWS's small GPU inference tier. It costs less than a p4, the kind of machine people bring in for huge training runs, and it is enough for a vision-language model on a small batch of photos.

Food photo captioning with BLIP is throughput over time. It is not trillion-parameter training. A T4, taking photos in groups of about eight, finishes a vendor folder of about thirty photos in one job. You do not have to provision a p3 you cannot fill.

The job definition in this course asks for four vCPUs, twelve thousand two hundred eighty-eight mebibytes, and one GPU. Batch then places one job on one whole instance. You are not bin-packing four separate one-GPU jobs onto a single g4dn. That optimization belongs to a large internal scheduler. It does not belong in this teaching pipeline. One folder, one job, one machine, one CSV. Debugging stays simpler, and the IAM story stays simpler, because a failure is one container on one box.

Fractional GPUs, or several jobs sharing one GPU, the way some Kubernetes setups do it, is a different lesson. Batch here is whole-instance placement through ECS. The container asks for the whole g4dn.xlarge, four vCPUs and one GPU, and that is the machine it gets.

About eight photos at a time is a memory choice inside that one job. It is still one T4, still one instance, still one CSV when the folder is done. You are not farming the folder out across a pool of smaller GPUs. Sixteen gibibytes of host memory is the box. Twelve thousand two hundred eighty-eight mebibytes is what the job is allowed to ask for, because ECS keeps some of the sixteen for the operating system and the agent. Four vCPUs is the whole machine, so the scheduler has nothing left on that instance to give a second GPU job. A bigger training box would leave most of the machine idle on a thirty-photo folder. A T4, groups of about eight, one job, matches the folder you actually have.

The host that pulls the image, and the Python that reads the photos, do not share one IAM role. Those two roles are next.
