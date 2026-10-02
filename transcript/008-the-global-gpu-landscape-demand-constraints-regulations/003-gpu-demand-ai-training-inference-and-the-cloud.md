# Video 003 — GPU Demand: AI Training, Inference and the Cloud

**Section:** 008 — The Global GPU Landscape: Demand, Constraints & Regulations
**Lecture#:** 003
**Sheet title:** GPU Demand: AI Training, Inference and the Cloud
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 008-003-gpu-demand-ai-training-infer

---

GPU demand has two main shapes: training and inference. They often compete for the same silicon, but they use it differently.

Training updates model weights across many GPUs for days or months. It needs fast interconnects such as NVLink and InfiniBand-class fabrics, synchronized computation, and checkpoints. A foundation-model run can occupy thousands of accelerators. This makes high-end training capacity scarce and encourages multi-year commitments.

Inference uses trained weights to produce results. Latency-sensitive applications keep models warm. Batch inference, like KodeFood, loads a model, processes a folder, and exits. Each run is small compared with frontier training, but popular products repeat inference continuously. In aggregate, that demand can become larger than training demand.

Cloud demand also includes graphics, scientific computing, video encoding, and recommendation systems. The `g4dn` is suited to inference and graphics rather than frontier training. That makes it appropriate for captioning, but it also puts KodeFood in the same capacity pool as other G-family users.

The distinction guides architecture. Long-running BLIP fine-tuning may justify reservations and a managed training platform. Captioning vendor folders points to Batch, Spot, and scale-to-zero. Combining both on one permanent fleet can waste capacity while serving neither workload well.

Training creates concentrated peaks; inference creates a broad, persistent load. Next we examine why much of both still runs through CUDA.

---

## Further reading (not spoken)

- [NVIDIA: AI Inference](https://www.nvidia.com/en-us/glossary/ai-inference/) — inference vs training in plain terms
- [AWS: Machine learning on AWS](https://aws.amazon.com/machine-learning/) — training and inference service map
- [IEA: Energy and AI](https://www.iea.org/reports/energy-and-ai) — how AI workload growth translates to infrastructure demand
