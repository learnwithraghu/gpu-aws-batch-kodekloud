# Video 001 — The Global GPU Supply Chain: From Chip Design to Cloud

**Section:** 008 — The Global GPU Landscape: Demand, Constraints & Regulations
**Lecture#:** 001
**Sheet title:** The Global GPU Supply Chain: From Chip Design to Cloud
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 008-001-the-global-gpu-supply-chain

---

The KodeFood job pulls an image from ECR and runs on a GPU in an AWS Region. Behind that simple action is a global supply chain. Seeing the chain makes a capacity shortage less mysterious.

The chain begins with architecture and software. NVIDIA designs GPUs and supplies CUDA, the programming model used by many PyTorch stacks. AMD Instinct, Intel Gaudi, AWS Trainium and Inferentia, and Google TPUs provide alternatives. CUDA still dominates many AI codebases, including our BLIP and PyTorch path.

Advanced foundries turn designs into silicon. TSMC fabricates a large share of leading-edge chips in Taiwan. A small group of suppliers also provides lithography equipment, high-bandwidth memory, substrates, packaging, and testing. Each stage has long lead times and limited substitutes. Disruption at one stage can later appear to a cloud customer as missing instance capacity.

Finished accelerators move into boards and servers, then into cloud data centers. Providers install racks, networking, power, and cooling before offering instances such as `g4dn` or `p5`. A cloud GPU is physical capital rented by the hour. Even a Spot bid depends on years of investment upstream.

Custom accelerators from companies such as Apple and Tesla still depend on many of the same foundries and suppliers. The chain is global, but several bottlenecks are concentrated.

When KodeFood waits in RUNNABLE, Regional inventory is the immediate cause, with this supply chain behind it. Next we look at why demand moved faster than supply.

---

## Further reading (not spoken)

- [TSMC: About TSMC](https://www.tsmc.com/english/aboutTSMC) — leading-edge foundry role in advanced chips
- [NVIDIA CUDA](https://www.nvidia.com/en-us/data-center/cuda/) — the software layer most AI frameworks target
- [ASML: About](https://www.asml.com/en/company) — extreme ultraviolet lithography in the supply chain
- [AWS: Inferentia and Trainium](https://aws.amazon.com/machine-learning/inferentia/) — cloud custom silicon as an alternative path
