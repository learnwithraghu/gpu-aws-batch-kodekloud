# Video 005 — GPU Availability Across AWS Regions and Cloud Providers

**Section:** 008 — The Global GPU Landscape: Demand, Constraints & Regulations
**Lecture#:** 005
**Sheet title:** GPU Availability Across AWS Regions and Cloud Providers
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 008-005-gpu-availability-across-aws

---

GPUs are not evenly poured across the map. Instance families, generations, and Spot depth differ by Region and by cloud. Your course lives in `ap-northeast-1` for a reason — it is a real Region with G-family stock — but “AWS has GPUs” never meant “every AZ has the SKU you want tonight.”

On AWS, check the instance type pages and the Service Quotas console per Region. Newer training giants — P5, P5e — land first in a handful of Regions. Older G4 and G5 spread wider but still thin out under load. Local Zones and Wavelength have different stories again. Batch only launches what the compute environment allows and what the AZ can sell. Multi-Region DR for GPU jobs is a product decision: replicate the image and data, accept that failover Region may have different capacity and pricing.

Other clouds rhyme. Azure’s N-series, Google Cloud’s A2/A3 and TPU pods, Oracle’s GPU shapes — each publishes regional matrices that change as inventory arrives. Independent trackers and status pages through the AI boom showed the same pattern: launch Regions rich, secondary Regions hungry, Spot flaky everywhere.

For KodeFood, regional choice also interacts with data residency — more on that soon — and with latency to S3. Keeping images, ECR, and Batch in one Region avoids cross-Region egress and surprise latency. If Tokyo Spot is dry, a second queue in another Region only helps if you also staged the photos there or accepted the transfer cost.

So availability is a matrix, not a boolean. Design for “preferred Region, documented fallback,” not for magical global GPU fluid. Where do those racks live physically, and what do they cost the planet? That is next — power, cooling, and the physical bill for AI.

---

## Further reading (not spoken)

- [AWS Regional Services](https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/) — which services and features exist where
- [Amazon EC2 instance types](https://aws.amazon.com/ec2/instance-types/) — GPU families and generations
- [Google Cloud: GPU regions](https://cloud.google.com/compute/docs/gpus/gpu-regions-zones) — example of per-Region accelerator matrices outside AWS
