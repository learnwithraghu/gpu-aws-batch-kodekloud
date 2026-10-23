# Video 005 — GPUs in the Cloud

**Section:** 002 — GPU Fundamentals: From Silicon to Cloud
**Lecture#:** 005
**Sheet title:** GPUs in the Cloud
**Type:** Video
**Runtime target:** ~3 minutes
**Topic code:** 002-005-gpus-in-the-cloud

---

Very few companies buy physical GPU servers just to process vendor menu photos. Instead, they rent GPUs in the cloud. But renting a GPU in AWS does not feel quite like renting an ordinary CPU instance.

Why is cloud GPU compute different in practice?

First, you are choosing a specific hardware profile. In AWS EC2, GPU instances are grouped into families. `G`-series instances—such as the `g4dn` family with NVIDIA T4 GPUs, or `g5` with A10G GPUs—are the workhorses for inference and single-GPU jobs like KodeFood. `P`-series instances pack multiple high-end GPUs with ultra-fast interconnects for massive model training, at a much higher hourly cost.

Second, a cloud GPU needs the right software layer on the host before your container even starts. If you boot a GPU instance with a plain Linux image that lacks NVIDIA drivers and container runtime hooks, the physical card is attached to the server, but your container sees zero GPUs.

Third, cloud GPUs are governed by strict capacity and account guardrails. Because accelerators are expensive and scarce, cloud providers separate on-demand capacity from spare Spot capacity, and they enforce tight GPU vCPU quotas—especially on new accounts, where the default on-demand GPU quota is often zero.

DoorDash and similar marketplace teams design around this reality: for offline catalog pipelines that arrive in bursts, you do not leave expensive GPU instances running twenty-four hours a day. You ask a scheduler like AWS Batch to spin up the right GPU instance when folders arrive, run the container with the NVIDIA driver stack in place, write the catalog CSV, and scale the fleet back to zero.

Notice how everything from this section now connects. A GPU gives us parallel tensor math and bounded VRAM; the cloud gives us on-demand access to that silicon; and AWS Batch gives us the control plane to run it only while work is waiting.

Next, we’ll step into the application layer and see how our container program is structured to run cleanly on top of this GPU setup.

---

## Further reading (not spoken)

- [AWS: Amazon EC2 Accelerated Computing Instance Types](https://aws.amazon.com/ec2/instance-types/#Accelerated_Computing) — overview of G-series and P-series GPU instances in AWS
- [AWS Batch User Guide: GPU Jobs](https://docs.aws.amazon.com/batch/latest/userguide/gpu-jobs.html) — how AWS Batch provisions NVIDIA-enabled EC2 instances for container workloads
- [AWS Service Quotas: Amazon EC2 Service Quotas](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-on-demand-instances-limits.html) — G and VT instance vCPU limits in AWS accounts
