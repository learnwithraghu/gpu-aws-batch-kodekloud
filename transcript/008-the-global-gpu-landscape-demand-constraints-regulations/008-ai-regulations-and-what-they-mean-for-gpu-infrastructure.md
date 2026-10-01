# Video 008 — AI Regulations and What They Mean for GPU Infrastructure

**Section:** 008 — The Global GPU Landscape: Demand, Constraints & Regulations
**Lecture#:** 008
**Sheet title:** AI Regulations and What They Mean for GPU Infrastructure
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 008-008-ai-regulations-and-what-they

---

Export controls police the chips. AI regulations police the systems — and they still land on your infrastructure checklist.

The EU AI Act is the clearest large-market example. It takes a risk-based approach: prohibited uses, high-risk systems with conformity duties, transparency rules for certain AI, and obligations around general-purpose models at the top end. Dates phase in over time; read the Official Journal and the Commission’s pages for the schedule that applies to you. For platform teams, “high-risk” can mean logging, human oversight, dataset documentation, and post-market monitoring — requirements that need durable storage, access control, and sometimes Region pinning, not only a clever model.

Elsewhere the picture fragments. The U.S. has executive orders, agency guidance, and sector rules rather than one AI statute. China has generative AI and algorithm filing regimes. Singapore, UK, Canada, and others publish codes and safety frameworks. Financial and health regulators add domain rules on top. None of these say “you must use Batch,” but they do say “prove what ran, on which data, with which model version.”

That is why our course obsesses over artifacts. S3 inputs, CSV outputs, job IDs, CloudWatch logs, immutable image digests in ECR — those are compliance building blocks. If a regulator asks how a vendor photo was rejected, you want a stem, a job, a model identity, and a row — not a forgotten notebook.

GPU infrastructure becomes the evidence plane. Training runs may need longer retention. Inference batches need reproducibility. Cross-border processing may be restricted even when GPUs are cheaper elsewhere.

So regulation turns architecture into accountability. Next we go deeper on one slice of that — data residency and sovereignty when AI crosses borders.

---

## Further reading (not spoken)

- [EU Artificial Intelligence Act](https://artificialintelligenceact.eu/) — accessible portal on the EU AI Act
- [European Commission: AI Act](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai) — official EU policy pages
- [Official Journal of the EU](https://eur-lex.europa.eu/) — authoritative legal text search
- [OECD AI Principles](https://oecd.ai/en/ai-principles) — international baseline many national frameworks reference
