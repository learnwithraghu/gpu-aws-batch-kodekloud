# Video 002 — Why There Is a GPU Capacity Problem

**Section:** 008 — The Global GPU Landscape: Demand, Constraints & Regulations
**Lecture#:** 002
**Sheet title:** Why There Is a GPU Capacity Problem
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 008-002-why-there-is-a-gpu-capacity-

---

You felt the capacity problem as a status: RUNNABLE with no instance. Zoom out and the same problem has three layers — manufacturing, cloud inventory, and account limits — stacked on top of each other.

Manufacturing first. Leading-edge wafers, HBM memory, and advanced packaging cannot scale as fast as chatbots went viral. Building a fab takes years and tens of billions of dollars. TSMC, memory makers, and OSAT partners publish capacity expansions, but those are multi-year curves, not weekend autoscaling. When every hyperscaler orders at once, someone waits.

Cloud inventory second. Even after chips exist, they must be racked, powered, cooled, and networked in a specific Availability Zone. AWS may have P5s in one Region and thin G4 stock in another. Spot capacity is leftover on-demand — great price, unpredictable depth. Your lesson Spot queue going quiet while Tokyo still has “GPUs somewhere” is exactly this: local pool empty, not planet empty.

Account limits third. Service Quotas — like on-demand G and VT instance limits — can be zero or tiny on a new account even when the Region has machines. You request increases; approval is not instant. That is policy capacity on top of physical capacity.

Add training clusters that hold thousands of GPUs for months. Those reservations remove flex inventory smaller jobs could have used. Reuters, Bloomberg, and company earnings calls through 2023–2025 repeated the theme: AI demand outpaced supply; delivery times stretched; cloud GPU waitlists became normal.

That's it here for the capacity squeeze: demand arrived faster than fabs, power, and cloud racks could answer. Next we split that demand into training versus inference — because they compete for the same silicon differently.

---

## Further reading (not spoken)

- [AWS Service Quotas](https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html) — account-level caps on instance families
- [AWS EC2: GPU instances](https://docs.aws.amazon.com/ec2/latest/instancetypes/ac.html) — which instance families carry NVIDIA GPUs
- [Semiconductor Industry Association](https://www.semiconductors.org/) — industry view on manufacturing capacity and policy
