# Video 006 — Data Centers, Power, Cooling and the Physical Cost of AI

**Section:** 008 — The Global GPU Landscape: Demand, Constraints & Regulations
**Lecture#:** 006
**Sheet title:** Data Centers, Power, Cooling and the Physical Cost of AI
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 008-006-data-centers-power-cooling-

---

A GPU job feels like JSON and containers. In the building, it is watts, water, and transformers. Understanding that physical layer explains why capacity cannot appear overnight even when the purchase order is signed.

Modern AI servers draw far more power per rack than classical web fleets. NVIDIA’s data-center GPUs are rated in hundreds of watts each; full HGX boards push kilowatts; dense racks need liquid cooling, not just raised-floor air. The International Energy Agency’s work on energy and AI, plus hyperscaler sustainability reports from AWS, Microsoft, and Google, all point the same direction: AI workloads are a material driver of new electricity demand, and grid interconnection queues can be longer than chip lead times.

Cooling is the twin constraint. Air hits limits; direct-to-chip liquid and immersion show up in new designs. Water usage and local permitting become community issues — you will see news from Virginia, Dublin, Singapore, and others about data-center growth versus residential power and water. The “cloud” has a zip code.

Carbon accounting follows. Providers publish Power Usage Effectiveness and carbon-free energy goals. Your Batch job’s footprint is tiny alone and real in aggregate. Scale-to-zero is not only a cost feature — idle GPUs still desire power if the instance is up. Turning capacity off when KodeFood’s queue is empty is an energy decision as much as a billing one.

That's it here for the physical bill: watts, cooling, and buildings constrain AI as much as chip roadmaps. Policy constrains it too. Next we open the geopolitics drawer — who is allowed to buy which accelerators.

---

## Further reading (not spoken)

- [IEA: Energy and AI](https://www.iea.org/reports/energy-and-ai) — electricity demand from AI and data centers
- [Amazon sustainability](https://sustainability.aboutamazon.com/) — AWS and Amazon environmental reporting
- [Microsoft: Sustainability](https://www.microsoft.com/en-us/sustainability) — hyperscaler energy and data-center disclosures
- [Google: Data center efficiency](https://www.google.com/about/datacenters/efficiency/) — PUE and cooling practices
