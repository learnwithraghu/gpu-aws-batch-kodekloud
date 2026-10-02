# Video 006 — Data Centers, Power, Cooling and the Physical Cost of AI

**Section:** 008 — The Global GPU Landscape: Demand, Constraints & Regulations
**Lecture#:** 006
**Sheet title:** Data Centers, Power, Cooling and the Physical Cost of AI
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 008-006-data-centers-power-cooling-

---

A GPU job appears as JSON and containers. Inside the data center, it is also electricity, cooling, and grid capacity. That physical layer explains why signed purchase orders do not create capacity overnight.

Modern AI servers draw much more power per rack than conventional web fleets. Individual data-center GPUs consume hundreds of watts, and multi-GPU systems consume kilowatts. Dense racks increasingly need liquid cooling. AI workloads now contribute materially to electricity demand, while grid connections can take longer to secure than chips.

Cooling is a second constraint. Air cooling reaches practical limits, so new facilities use direct-to-chip liquid systems or immersion. Water use and permitting can put data-center growth in conflict with local power and water needs. The cloud always occupies a physical place.

Providers therefore track measures such as Power Usage Effectiveness and publish clean-energy goals. One KodeFood Batch job has a small footprint, but repeated jobs add up. Scale-to-zero reduces both cost and energy use because an idle running instance still consumes power.

Chips are only one limit; power, cooling, and buildings set limits too. Next we turn to policy and who may buy or access advanced accelerators.

---

## Further reading (not spoken)

- [IEA: Energy and AI](https://www.iea.org/reports/energy-and-ai) — electricity demand from AI and data centers
- [Amazon sustainability](https://sustainability.aboutamazon.com/) — AWS and Amazon environmental reporting
- [Microsoft: Sustainability](https://www.microsoft.com/en-us/sustainability) — hyperscaler energy and data-center disclosures
- [Google: Data center efficiency](https://www.google.com/about/datacenters/efficiency/) — PUE and cooling practices
