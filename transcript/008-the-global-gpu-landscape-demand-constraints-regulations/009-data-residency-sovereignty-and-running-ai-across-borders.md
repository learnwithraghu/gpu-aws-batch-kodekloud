# Video 009 — Data Residency, Sovereignty and Running AI Across Borders

**Section:** 008 — The Global GPU Landscape: Demand, Constraints & Regulations
**Lecture#:** 009
**Sheet title:** Data Residency, Sovereignty and Running AI Across Borders
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 008-009-data-residency-sovereignty-

---

Suppose Tokyo Spot is dry and Seoul has G instances. Can KodeFood simply process Japanese vendor photos in another country? Maybe technically. Maybe not legally. Data residency and sovereignty are the rules about where data may live and who may compel access to it.

Residency usually means “this personal or regulated data stays in-Region.” GDPR does not ban all transfers, but it constrains them — adequacy decisions, standard contractual clauses, transfer impact assessments. Sector rules can be stricter: financial records, health data, tax identifiers. Sovereignty conversations go further — governments wanting local operations, local keys, or assurance that foreign law enforcement cannot quietly reach the disks. AWS answers with Regions, Local Zones, and offerings like AWS European Sovereign Cloud for customers with heightened requirements; other hyperscalers have parallel programs.

For GPU pipelines the trap is accidental egress. A job in Region A that pulls training data from Region B, writes embeddings to a global bucket, or phones home to a model API in a third country has moved data even if the engineer only “wanted capacity.” Logs and crash dumps can leak payloads too. Keep images, CSV catalogs, ECR mirrors, and CloudWatch in the approved Region unless legal and security signed off on the path.

Practical pattern for marketplace photos: classify the data. Public menu shots may travel more freely than government ID selfies. KodeFood’s teaching set is vendor food photos — still treat location as a first-class design choice, not an afterthought when RUNNABLE hurts.

That's it here for residency: where bytes and models live is a product decision, not only a compliance checkbox. Underneath every Region choice sits another constraint — the price of the silicon itself. Next: why GPU compute feels expensive even in the cloud.

---

## Further reading (not spoken)

- [AWS: Data residency](https://aws.amazon.com/compliance/data-residency/) — how AWS frames Regional data control
- [AWS European Sovereign Cloud](https://aws.amazon.com/compliance/europe-digital-sovereignty/) — example sovereign offering
- [European Commission: GDPR](https://commission.europa.eu/law/law-topic/data-protection_en) — personal data transfer context
- [AWS Batch](https://docs.aws.amazon.com/batch/) — keep compute next to approved data Regions
