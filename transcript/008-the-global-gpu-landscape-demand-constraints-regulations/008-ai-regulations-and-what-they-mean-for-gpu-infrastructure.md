# Video 008 — AI Regulations and What They Mean for GPU Infrastructure

**Section:** 008 — The Global GPU Landscape: Demand, Constraints & Regulations
**Lecture#:** 008
**Sheet title:** AI Regulations and What They Mean for GPU Infrastructure
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 008-008-ai-regulations-and-what-they

---

Export controls shape access to chips. AI regulations shape how systems using those chips are governed. Both reach the infrastructure team.

The EU AI Act is a prominent example. It uses a risk-based structure covering prohibited uses, high-risk systems, transparency duties, and obligations for some general-purpose models. Its requirements phase in, so teams must check the current official schedule. For a platform team, compliance may require logs, human oversight, dataset records, post-market monitoring, access controls, and Regional restrictions.

Other jurisdictions use different combinations of laws, agency guidance, filing regimes, sector rules, and safety frameworks. The details vary, but a common infrastructure need is evidence: what ran, which data it used, and which model version produced the result.

KodeFood already creates useful evidence. S3 holds the inputs and CSV outputs. Batch records a job ID. CloudWatch keeps execution logs. An immutable ECR digest can identify the container. The BLIP model revision must also be pinned or recorded; the container digest alone cannot identify weights downloaded at runtime. Together, those artifacts can explain how a vendor photo was processed far better than an untracked notebook.

Infrastructure becomes part of the evidence plane. Training records may need long retention. Inference batches need reproducibility. Cross-border processing may remain restricted even when another Region is cheaper.

Regulation turns architecture decisions into accountability records. Next we focus on data residency and sovereignty across borders.

---

## Further reading (not spoken)

- [EU Artificial Intelligence Act](https://artificialintelligenceact.eu/) — accessible portal on the EU AI Act
- [European Commission: AI Act](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai) — official EU policy pages
- [Official Journal of the EU](https://eur-lex.europa.eu/) — authoritative legal text search
- [OECD AI Principles](https://oecd.ai/en/ai-principles) — international baseline many national frameworks reference
