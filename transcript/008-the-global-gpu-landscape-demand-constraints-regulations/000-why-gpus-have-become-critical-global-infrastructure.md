# Video 000 — Why GPUs Have Become Critical Global Infrastructure

**Section:** 008 — The Global GPU Landscape: Demand, Constraints & Regulations
**Lecture#:** 000
**Sheet title:** Why GPUs Have Become Critical Global Infrastructure
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 008-000-why-gpus-have-become-critic

---

Batch, ECS, EKS, and SageMaker all depend on the same thing: an available accelerator. When the KodeFood job remains RUNNABLE in Tokyo, a small application is meeting a global infrastructure constraint.

A decade ago, GPUs were associated mainly with graphics and specialized scientific computing. Today they train foundation models, serve inference, simulate proteins, price risk, and rank recommendations. The same class of chip that renders a game can calculate attention in a transformer. That range of uses has turned GPU clusters into strategic capacity.

Cloud providers are investing heavily in accelerators. Research labs compete for cluster time. Governments fund AI factories and sovereign clouds. Compute is no longer a background resource; it is a constrained input to economic and national plans.

KodeFood shows the practical response. It uses finite inference jobs, prefers Spot capacity, and scales toward zero. Captioning vendor dishes does not need a supercluster. It needs a small amount of reliable GPU time, followed by no GPU bill at all.

Treat accelerator capacity as a dependency, not an assumption. Next we follow the supply chain from chip design to the cloud rack that runs the Batch job.

---

## Further reading (not spoken)

- [NVIDIA: Data Center](https://www.nvidia.com/en-us/data-center/) — how NVIDIA frames GPUs as AI infrastructure
- [International Energy Agency: Energy and AI](https://www.iea.org/reports/energy-and-ai) — global view of AI-driven electricity demand
- [AWS Batch User Guide](https://docs.aws.amazon.com/batch/) — the scheduling layer you use on top of scarce GPU capacity
