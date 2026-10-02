# Video 005 — GPU Availability Across AWS Regions and Cloud Providers

**Section:** 008 — The Global GPU Landscape: Demand, Constraints & Regulations
**Lecture#:** 005
**Sheet title:** GPU Availability Across AWS Regions and Cloud Providers
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 008-005-gpu-availability-across-aws

---

GPU capacity is uneven. Instance families, hardware generations, and Spot depth differ by Region, Availability Zone, and cloud provider. KodeFood runs in `ap-northeast-1`, but the presence of G-family instances in AWS does not guarantee that the required SKU is available in every pool.

On AWS, instance availability and Service Quotas are Regional. New training families such as P5 and P5e first appear in a limited set of Regions. G4 and G5 are more widely distributed, but can still become scarce. Local Zones and Wavelength have separate inventories. Batch can launch only the instance types allowed by the compute environment and available in its configured locations.

Other providers follow the same pattern. Azure N-series, Google Cloud A2 and A3 instances and TPU pods, and Oracle GPU shapes all have Regional matrices that change as inventory expands. Major launch Regions tend to receive capacity first, while Spot remains variable.

For KodeFood, failover is more than creating a second queue. Images, the ECR image, and output storage must also be available in the fallback Region, or the system must accept transfer latency and cost. Data-residency rules may further limit that move.

Availability is a matrix, not a yes-or-no property. A sound plan names the preferred Region, the permitted fallback, and the data-movement cost. Next we examine the power and cooling behind those Regional pools.

---

## Further reading (not spoken)

- [AWS Regional Services](https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/) — which services and features exist where
- [Amazon EC2 instance types](https://aws.amazon.com/ec2/instance-types/) — GPU families and generations
- [Google Cloud: GPU regions](https://cloud.google.com/compute/docs/gpus/gpu-regions-zones) — example of per-Region accelerator matrices outside AWS
