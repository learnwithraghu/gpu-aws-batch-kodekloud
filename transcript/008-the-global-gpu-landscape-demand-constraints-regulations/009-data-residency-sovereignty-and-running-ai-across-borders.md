# Video 009 — Data Residency, Sovereignty and Running AI Across Borders

**Section:** 008 — The Global GPU Landscape: Demand, Constraints & Regulations
**Lecture#:** 009
**Sheet title:** Data Residency, Sovereignty and Running AI Across Borders
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 008-009-data-residency-sovereignty-

---

Suppose Tokyo Spot capacity is unavailable while Seoul has G instances. KodeFood may be able to move the job technically, but the data may not be allowed to move. Residency governs where data is stored or processed. Sovereignty also considers which jurisdiction can compel access.

Residency requirements often keep personal or regulated data in an approved Region. GDPR permits some transfers under defined safeguards, while financial, health, or tax rules may be stricter. Sovereignty requirements can add local operations, local encryption keys, or protection from foreign legal access. Cloud providers respond with Regions, Local Zones, and sovereign-cloud offerings.

GPU pipelines can create accidental egress. A job may pull data from another Region, write embeddings elsewhere, call an API in a third country, or include payloads in logs and crash dumps. Keep images, CSV catalogs, ECR mirrors, and CloudWatch logs in the approved Region unless legal and security teams approve another path.

Start by classifying the data. Public menu photos may have fewer restrictions than identity documents. KodeFood uses vendor food photos, but processing location should still be an explicit design choice rather than an emergency response to RUNNABLE jobs.

Where data and models live is both a product and compliance decision. Next we examine the economics behind the Regional GPU price.

---

## Further reading (not spoken)

- [AWS: Data residency](https://aws.amazon.com/compliance/data-residency/) — how AWS frames Regional data control
- [AWS European Sovereign Cloud](https://aws.amazon.com/compliance/europe-digital-sovereignty/) — example sovereign offering
- [European Commission: GDPR](https://commission.europa.eu/law/law-topic/data-protection_en) — personal data transfer context
- [AWS Batch](https://docs.aws.amazon.com/batch/) — keep compute next to approved data Regions
