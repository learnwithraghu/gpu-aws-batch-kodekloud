# Video 010 — The Economics of GPUs: Why GPU Compute Is Expensive

**Section:** 008 — The Global GPU Landscape: Demand, Constraints & Regulations
**Lecture#:** 010
**Sheet title:** The Economics of GPUs: Why GPU Compute Is Expensive
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 008-010-the-economics-of-gpus-why-g

---

A GPU instance costs far more than a comparable CPU instance because its hourly price carries an expensive physical stack.

A data-center GPU can cost thousands of dollars, while a multi-GPU server can cost tens or hundreds of thousands before networking. Cloud providers must recover that capital expense. The hourly rate also covers network interfaces, optics, racks, power, cooling, facilities, and operations. Limited supply adds a scarcity premium.

Utilization determines whether that price produces value. A GPU kept warm for an interactive service may sit idle between requests while billing continues. KodeFood avoids that pattern by renting capacity for the caption window and scaling toward zero afterward. Spot lowers the price in exchange for interruption risk. On-demand capacity is more predictable, but it can still be unavailable. Reservations and savings commitments suit steady workloads better than bursty vendor onboarding.

Software overhead also consumes paid minutes. Large CUDA images, model downloads, and cold starts delay the first useful caption. Micro-batching and moving I/O away from the GPU's critical path improve unit economics.

The KodeFood CSV makes the unit visible: GPU cost per folder, or per accepted caption. That measure connects infrastructure choices to product economics.

GPU expense combines capital cost, scarcity, and idle risk. The final lesson asks whether the industry answers with more hardware, better efficiency, or both.

---

## Further reading (not spoken)

- [Amazon EC2 pricing](https://aws.amazon.com/ec2/pricing/) — on-demand vs Spot vs savings constructs
- [AWS Batch: Spot best practices](https://docs.aws.amazon.com/batch/latest/userguide/spot_best_practice.html) — using interruptible capacity for batch work
- [NVIDIA investor relations](https://investor.nvidia.com/) — primary disclosures on data-center GPU demand and pricing power
