# Video 003 — GPU Demand: AI Training, Inference and the Cloud

**Section:** 008 — The Global GPU Landscape: Demand, Constraints & Regulations
**Lecture#:** 003
**Sheet title:** GPU Demand: AI Training, Inference and the Cloud
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 008-003-gpu-demand-ai-training-infer

---

Not all GPU demand looks the same. Training and inference fight for the same chips with different shapes — and the cloud sells both by the hour.

Training is the heavy lift. You update model weights across many GPUs for days or months. Clusters want fast interconnect — NVLink, InfiniBand-class fabrics — synchronized steps, and checkpoints. One foundation-model run can lock thousands of accelerators. That is why P5-class and similar training SKUs book out, and why labs sign multi-year cloud deals. Training demand is lumpy, prestigious, and sticky.

Inference is the long tail. After weights exist, every user request or batch job runs the forward pass. Latency-sensitive apps keep models warm on endpoints. Batch inference — our KodeFood path — loads a model, processes a folder, exits. Individually small; in aggregate, inference can exceed training FLOPs once a model is popular. Goldman Sachs, McKinsey, and hyperscaler blogs have all argued that inference spend grows as products ship, even if training headlines dominate.

Cloud demand is the sum plus everything else: graphics, classical HPC, video encode, recommendation ranking. Your `g4dn` is an inference-and-graphics sweet spot, not a frontier training box — which is why it fits captioning and why it still competes with game streaming and other G-family users.

For architecture, the split is a decision tool. Are you fine-tuning BLIP for months? Think training reservations and managed training platforms. Are you captioning vendor folders all day? Think Batch, Spot, scale to zero — do not hold a training cluster for product inference. Mixing the two on one always-on fleet is how teams waste money and still miss SLAs.

So demand is not one number. It is training spikes plus inference oceans. Next: why so much of that ocean still speaks NVIDIA’s language — CUDA.

---

## Further reading (not spoken)

- [NVIDIA: AI Inference](https://www.nvidia.com/en-us/glossary/ai-inference/) — inference vs training in plain terms
- [AWS: Machine learning on AWS](https://aws.amazon.com/machine-learning/) — training and inference service map
- [IEA: Energy and AI](https://www.iea.org/reports/energy-and-ai) — how AI workload growth translates to infrastructure demand
