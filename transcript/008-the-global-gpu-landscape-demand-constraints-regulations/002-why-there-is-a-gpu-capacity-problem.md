# Video 002 — Why There Is a GPU Capacity Problem

**Section:** 008 — The Global GPU Landscape: Demand, Constraints & Regulations
**Lecture#:** 002
**Sheet title:** Why There Is a GPU Capacity Problem
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 008-002-why-there-is-a-gpu-capacity-

---

For KodeFood, the capacity problem appeared as RUNNABLE with no instance. That status can come from three layers: manufacturing supply, cloud inventory, and account limits.

Manufacturing is the slowest layer. Leading-edge wafers, high-bandwidth memory, and advanced packaging cannot expand on software timelines. A fabrication plant takes years and billions of dollars to build. Capacity grows over multi-year cycles, so simultaneous orders from cloud providers create queues.

Cloud inventory is the next layer. Chips must be installed, powered, cooled, and networked in a particular Availability Zone. One Region may have P5 capacity while another has limited G4 stock. Spot draws from spare capacity, so its price is attractive and its depth is unpredictable. An empty Tokyo pool does not mean the world has no GPUs.

Account limits form the third layer. Service Quotas for on-demand G and VT families may be zero or small in a new account, even when AWS has hardware in the Region. A quota increase takes time. This is administrative capacity layered over physical capacity.

Large training clusters can reserve thousands of GPUs for months, reducing flexible inventory for smaller jobs. During the AI expansion of 2023–2025, demand outpaced delivery and cloud waitlists became common.

When a job stalls, diagnose the layers in order: job requirements, account quota, Regional inventory, then the broader supply constraint. Next we separate training demand from inference demand.

---

## Further reading (not spoken)

- [AWS Service Quotas](https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html) — account-level caps on instance families
- [AWS EC2: GPU instances](https://docs.aws.amazon.com/ec2/latest/instancetypes/ac.html) — which instance families carry NVIDIA GPUs
- [Semiconductor Industry Association](https://www.semiconductors.org/) — industry view on manufacturing capacity and policy
