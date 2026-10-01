# Video 010 — The Economics of GPUs: Why GPU Compute Is Expensive

**Section:** 008 — The Global GPU Landscape: Demand, Constraints & Regulations
**Lecture#:** 010
**Sheet title:** The Economics of GPUs: Why GPU Compute Is Expensive
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 008-010-the-economics-of-gpus-why-g

---

Open the EC2 pricing page for a GPU instance next to a similar CPU instance. The gap looks rude until you price the stack behind it.

Start with the bill of materials. An NVIDIA data-center GPU can cost many thousands of dollars at the card; a full multi-GPU server lands in the tens or hundreds of thousands before networking. Hyperscalers buy at scale and still need return on that CapEx. Your hourly rate amortizes chips, NICs, optics, racks, power, cooling, buildings, and the people who keep them alive. Scarcity raises clearing prices — classic supply and demand on a multi-year manufacturing lag.

Then utilization. A CPU fleet for web APIs can run hot with many tenants. A GPU held for a warm chatbot may sit at low duty cycle between requests — and you still pay. That is why Batch’s scale-to-zero and Spot matter for KodeFood: you convert “own a fraction of an expensive machine forever” into “rent it for the caption window.” Spot discounts exist because you accept interruption; on-demand premiums buy certainty. Reserved and savings plans help steady training farms, not bursty vendor onboarding.

Software taxes hide in the image. Large CUDA bases, model weights pulled at runtime, longer cold starts — all burn GPU minutes before the first useful caption. Micro-batching and keeping I/O off the critical path are economic moves, not only engineering aesthetics.

Public references — NVIDIA earnings, cloud pricing pages, and analyses from groups like a16z or SemiAnalysis — repeat the refrain: AI CapEx is enormous; inference unit economics decide who profits. Your CSV pipeline is a unit-economics story in miniature.

So GPU expense is CapEx scarcity plus idle risk. The finale asks where this goes — more GPUs forever, or better efficiency — and how what you built already votes.

---

## Further reading (not spoken)

- [Amazon EC2 pricing](https://aws.amazon.com/ec2/pricing/) — on-demand vs Spot vs savings constructs
- [AWS Batch: Spot best practices](https://docs.aws.amazon.com/batch/latest/userguide/spot_best_practice.html) — using interruptible capacity for batch work
- [NVIDIA investor relations](https://investor.nvidia.com/) — primary disclosures on data-center GPU demand and pricing power
