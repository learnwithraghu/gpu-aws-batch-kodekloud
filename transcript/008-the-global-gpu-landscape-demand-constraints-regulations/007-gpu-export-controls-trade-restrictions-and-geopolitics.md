# Video 007 — GPU Export Controls, Trade Restrictions and Geopolitics

**Section:** 008 — The Global GPU Landscape: Demand, Constraints & Regulations
**Lecture#:** 007
**Sheet title:** GPU Export Controls, Trade Restrictions and Geopolitics
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 008-007-gpu-export-controls-trade-r

---

Chips move through trade law as carefully as through factories. Since 2022, the U.S. Bureau of Industry and Security — BIS — has tightened export controls on advanced semiconductors and manufacturing tools bound for certain destinations, with updates through subsequent years. High-end AI GPUs, and sometimes “tuned” variants below a performance threshold, sit in that policy crosshair. Allies coordinated; China and others answered with their own procurement and industrial policies. The details change — always read the current Federal Register and BIS notices — but the shape is stable: leading AI accelerators are dual-use technology in the eyes of governments.

What does that mean for a cloud engineer? Hyperscalers must comply when placing hardware and when offering certain instances in certain Regions or to certain customers. Product availability can lag or differ by geography for legal reasons, not only for inventory. If you build a global SaaS on GPU inference, your Region matrix may be constrained by export classification as much as by latency. NVIDIA has publicly discussed complying with U.S. rules and shipping compliant SKUs; that is geopolitics showing up in the EC2 dropdown.

Allied industrial policy cuts the other way — U.S. CHIPS programs, the EU Chips Act, Japan and Korea investments — rebalancing foundry capacity over years. Short term, controls tighten supply for some buyers while everyone else still queues for the same wafers.

KodeFood in Tokyo on a G4-class instance is not a sanctions case study. The lesson still lands: assume accelerator access can be policy-gated, document where you run, and avoid architectures that require unrestricted access to the absolute newest training SKU in every country.

Who regulates the models those GPUs run? That is the next lecture — AI Acts and what they imply for infrastructure teams.

---

## Further reading (not spoken)

- [U.S. Bureau of Industry and Security](https://www.bis.doc.gov/) — primary U.S. export control authority
- [BIS: Semiconductor and advanced computing rules](https://www.bis.doc.gov/index.php/documents/regulations-docs) — start from BIS publications for current GPU-related rules
- [U.S. CHIPS Program Office](https://www.nist.gov/chips) — industrial policy context for domestic semiconductor capacity
- [European Chips Act](https://digital-strategy.ec.europa.eu/en/policies/european-chips-act) — EU semiconductor policy counterpart
