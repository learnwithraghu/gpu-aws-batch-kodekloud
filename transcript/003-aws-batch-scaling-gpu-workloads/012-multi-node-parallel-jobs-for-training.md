# Video 012 — Multi-Node Parallel Jobs for Training

**Section:** 003 — AWS Batch: Scaling GPU Workloads
**Lecture#:** 012
**Sheet title:** Multi-Node Parallel Jobs for Training
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 003-012-multi-node-parallel-jobs-for-t

---

KodeFood captioning fits on one GPU. Large model training often does not.

So what changes when a single machine is no longer enough?

You move from embarrassingly parallel jobs to coordinated parallel jobs. Array jobs are independent children. Each vendor folder can succeed or fail alone. Multi-node parallel jobs are different. Batch launches a group of nodes together so distributed training can share gradients and progress as one logical run.

Why does that distinction matter?

Because the failure and scheduling models change. If one node in a training gang never comes up, the whole training attempt may be useless. Capacity has to appear as a set, not as random leftover holes in the kitchen. Networking and interconnect expectations also rise far above what a single inference box needs.

Netflix-style offline scoring and KodeFood inference usually stay in the single-node or array world. Multi-node parallel is the tool you reach for when the model itself must span machines during one training job.

Keep the boundary crisp. Fan out independent catalog folders with arrays. Train a model across many GPUs with multi-node parallel. Do not force training semantics onto a marketplace caption burst, and do not pretend a giant training run is “just another array index.”

For this course, remember that Batch can do both shapes — then stay honest about which shape KodeFood actually needs.

Next, we return to cost. Even single-GPU inference gets expensive if you always pay on-demand prices, so we look at cutting GPU spend with Spot.

---

## Further reading (not spoken)

- [AWS Batch: Multi-node parallel jobs](https://docs.aws.amazon.com/batch/latest/userguide/multi-node-parallel-jobs.html) — gang-scheduled distributed workloads
- [AWS Batch: Array jobs](https://docs.aws.amazon.com/batch/latest/userguide/array_jobs.html) — independent fan-out contrasted with MNP
- [Amazon EC2 P-series instances](https://aws.amazon.com/ec2/instance-types/#Accelerated_Computing) — multi-GPU training shapes often paired with MNP
