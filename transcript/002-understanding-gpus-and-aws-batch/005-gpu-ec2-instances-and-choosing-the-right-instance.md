# Video 005 — GPU EC2 Instances and Choosing the Right Instance
**Section:** 002 — Understanding GPUs and AWS Batch
**Lecture#:** 005
**Sheet title:** GPU EC2 Instances and Choosing the Right Instance
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 002-005-gpu-ec2-instances-and-choosing

---

Batch’s compute environment only helps if we pick an instance shape that matches the work. Let’s choose deliberately.

AWS offers several GPU families. Broadly, `g4dn` instances pair NVIDIA T4 GPUs with practical amounts of host memory — strong for inference and graphics-style workloads. `g5` instances step up to NVIDIA A10G GPUs with more performance and usually more cost. Training-oriented families exist too; they are overkill for captioning thirty menu photos.

For KodeFood we standardize on `g4dn.xlarge`: four vCPUs, sixteen GiB of host memory, one T4. That is enough to hold BLIP and micro-batches of eight. In the job definition we ask for the whole machine’s useful CPU and one GPU, and we cap container memory at twelve thousand two hundred eighty-eight MiB so placement succeeds. Asking for sixteen thousand three hundred eighty-four MiB looks tidy on paper and fails in practice — the host cannot give the container every byte.

Notice the decision rule. Match GPU generation to the model size and latency you need, match host memory to the container plus the OS, and prefer the smallest instance that finishes the folder comfortably. Jumping to `g5` without a measured need mostly buys a larger bill. For captioning a few dozen menu photos, the T4 is the right altitude.

One more practical note: in Batch we treat one catalog job as owning that whole `g4dn.xlarge`. We are not packing several GPU jobs onto one box in this course. That keeps placement simple while you learn the pipeline.

That’s it here for instance choice. Even the right `g4dn` still forces another fork: do we buy that capacity as Spot or on-demand? Next we compare those two purchase models for GPU compute.

---

## Further reading (not spoken)

- https://aws.amazon.com/ec2/instance-types/g4/ — G4 instance family and T4 positioning
- https://aws.amazon.com/ec2/instance-types/g5/ — G5 family for contrast
- https://www.nvidia.com/en-us/data-center/tesla-t4/ — T4 as an inference-oriented GPU
