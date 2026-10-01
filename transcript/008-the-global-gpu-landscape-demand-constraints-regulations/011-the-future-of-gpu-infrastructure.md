# Video 011 — The Future of GPU Infrastructure: More GPUs or Better Efficiency?

**Section:** 008 — The Global GPU Landscape: Demand, Constraints & Regulations
**Lecture#:** 011
**Sheet title:** The Future of GPU Infrastructure: More GPUs or Better Efficiency?
**Type:** Video
**Runtime target:** ~3 minutes
**Topic code:** 008-011-the-future-of-gpu-infrastruc

---

We end on a fork the whole industry is arguing about. Will the future of GPU infrastructure be mostly “pour more silicon into more buildings,” or mostly “do more useful work per watt and per dollar”? Honest answer: both — but your architecture has to pick a bias, and this course already did.

The “more GPUs” path is real. NVIDIA and competitors roadmap denser packages. TSMC and peers build new fabs. Hyperscalers announce multi-gigawatt campuses. Sovereign funds finance national clusters. Training the next generation of models will still want bigger contiguous fabrics. If your job is frontier research, you live on that path — reservations, specialized networking, multi-year capacity deals.

The “better efficiency” path is just as real. Quantization, distillation, smaller task models, batching, speculative decoding, custom inference chips, better schedulers, and turning machines off when queues drain. The IEA and hyperscaler sustainability teams keep saying the quiet part: grids and capital cannot scale naively with every token. Product companies win when a good-enough model on a G-class instance beats a giant model held warm for vanity.

Look at what you built for KodeFood through that lens. You did not reserve a permanent training cluster to caption dish photos. You containerized inference, stored inputs and outputs on S3, scheduled with AWS Batch, preferred Spot, sized memory so jobs place, and let `minvCpus` fall toward zero when nothing runs. That is an efficiency-shaped production system. When RUNNABLE hurt, you learned capacity is scarce — then you designed for scarce, not against it.

Zoom across the section. Supply chains and geopolitics will keep wobbling the SKU list. AI Acts and residency rules will keep demanding logs, digests, and Regional discipline. Economics will keep punishing idle accelerators. In that world, the teams that survive are not only the ones with the biggest cluster purchase order. They are the ones who know when a job should be a job, when a GPU should be dark, and when “good enough caption” beats “largest model.”

Carry three habits out of this course. One: treat the container digest and the S3 contract as the product truth. Two: measure queue time and GPU busy time, not only success rate. Three: choose Batch-like scale-to-zero for burst inference, and reserve always-on GPUs only when latency economics prove they earn their keep.

The global GPU landscape will keep changing — new chips, new rules, new Regions. The KodeFood pattern travels: scarce accelerators, durable data, finite jobs, honest utilization. You built that end to end. Now go put it to work — and keep asking, every architecture review, whether you are buying more silicon or buying more judgment.

---

## Further reading (not spoken)

- [AWS Batch User Guide](https://docs.aws.amazon.com/batch/) — scale-out and scale-toward-zero batch scheduling
- [IEA: Energy and AI](https://www.iea.org/reports/energy-and-ai) — why efficiency competes with raw capacity growth
- [NVIDIA CUDA](https://www.nvidia.com/en-us/data-center/cuda/) — the software stack most efficiency work still targets today
- [EU AI Act portal](https://artificialintelligenceact.eu/) — accountability pressures that reward logged, finite inference jobs
- [Amazon sustainability](https://sustainability.aboutamazon.com/) — physical footprint context for always-on vs on-demand compute
