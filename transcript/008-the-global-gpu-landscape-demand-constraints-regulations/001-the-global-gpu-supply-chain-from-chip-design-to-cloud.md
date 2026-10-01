# Video 001 — The Global GPU Supply Chain: From Chip Design to Cloud

**Section:** 008 — The Global GPU Landscape: Demand, Constraints & Regulations
**Lecture#:** 001
**Sheet title:** The Global GPU Supply Chain: From Chip Design to Cloud
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 008-001-the-global-gpu-supply-chain

---

Your Batch job pulls an image from ECR and runs on a GPU in an AWS Region. That sentence hides a planet-scale supply chain. Walk it once so capacity problems stop feeling like random console weather.

It starts with architecture and software. NVIDIA designs the GPU and ships CUDA — the programming model almost every PyTorch stack assumes. Competitors exist — AMD Instinct, Intel Gaudi, cloud custom silicon like AWS Trainium and Inferentia, Google TPUs — but the CUDA ecosystem still dominates many AI codebases, including ours with BLIP on PyTorch.

Those designs become silicon at advanced foundries. TSMC fabricates a huge share of leading-edge chips in Taiwan, with packaging and memory partners in a tight regional web. ASML’s lithography machines, HBM memory from a few suppliers, substrates, and testing — each step has few factories and long lead times. A war, earthquake, or export rule at any hop shows up months later as “no G instances in this Region.”

Finished accelerators go into boards and servers — often NVIDIA HGX or partner systems — then into hyperscaler data centers. AWS, Microsoft Azure, Google Cloud, and others buy at enormous scale, install racks, wire networking and liquid cooling, and finally rent you a `g4dn` or `p5` by the hour. Cloud is not “virtual GPUs from nowhere.” It is someone else’s capital expenditure, amortized into your Spot bid.

Apple, Tesla, and others also design custom accelerators — same foundry dependencies. The chain is global; the bottlenecks are local and few.

So when KodeFood waits RUNNABLE, you are waiting on that chain plus regional inventory. Next: why demand outran supply — and why that imbalance became normal.

---

## Further reading (not spoken)

- [TSMC: About TSMC](https://www.tsmc.com/english/aboutTSMC) — leading-edge foundry role in advanced chips
- [NVIDIA CUDA](https://www.nvidia.com/en-us/data-center/cuda/) — the software layer most AI frameworks target
- [ASML: About](https://www.asml.com/en/company) — extreme ultraviolet lithography in the supply chain
- [AWS: Inferentia and Trainium](https://aws.amazon.com/machine-learning/inferentia/) — cloud custom silicon as an alternative path
