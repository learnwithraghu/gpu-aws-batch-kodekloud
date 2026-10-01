# Video 000 — Why GPUs Have Become Critical Global Infrastructure

**Section:** 008 — The Global GPU Landscape: Demand, Constraints & Regulations
**Lecture#:** 000
**Sheet title:** Why GPUs Have Become Critical Global Infrastructure
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 008-000-why-gpus-have-become-critic

---

You just compared Batch, ECS, EKS, and SageMaker. Under every option sat the same scarce machine: a GPU instance that may not be there when your job turns RUNNABLE. This section zooms out. Why does one vendor photo pipeline in Tokyo care about global infrastructure politics? Because the accelerator in that g4dn is part of a worldwide bottleneck.

A decade ago, GPUs were “graphics cards” and a niche for scientific computing. Today they are the default engines for training foundation models, running inference at user scale, simulating proteins, pricing risk, and recommending the next video. The same chip class that draws frames in a game now draws attention maps in a transformer. Nations talk about GPU clusters the way they once talked about shipyards or semiconductor fabs — as strategic capacity.

Public signals are loud. Hyperscalers publish capital plans heavy on accelerators. Labs compete for cluster time. Governments fund AI factories and sovereign clouds. When NVIDIA frames the GPU as the engine of AI factories, compute is the scarce input — not an afterthought.

For KodeFood the lesson is practical. Your design — scale to zero, Spot first, finite jobs, inference not endless training — is how ordinary product teams survive in that world. You do not need a supercluster to caption vendor dishes. You need reliable access to a little GPU for a little while, then nothing. That is infrastructure literacy: know what is scarce, then build so scarcity does not bankrupt the product.

Critical infrastructure means power grids, networks, and now accelerators. Treat them that way in architecture reviews. Next we follow one chip from design to the cloud rack — who actually builds the path your Batch job depends on.

---

## Further reading (not spoken)

- [NVIDIA: Data Center](https://www.nvidia.com/en-us/data-center/) — how NVIDIA frames GPUs as AI infrastructure
- [International Energy Agency: Energy and AI](https://www.iea.org/reports/energy-and-ai) — global view of AI-driven electricity demand
- [AWS Batch User Guide](https://docs.aws.amazon.com/batch/) — the scheduling layer you use on top of scarce GPU capacity
