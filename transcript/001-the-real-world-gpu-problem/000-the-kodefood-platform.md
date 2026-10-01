# Video 000 — The KodeFood Platform
**Section:** 001 — The Real-World GPU Problem
**Lecture#:** 000
**Sheet title:** The KodeFood Platfrom
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 001-000-the-kodefood-platfrom

---

Welcome to Building Production GPU Workloads on AWS.

In this course we build something real — one product problem all the way into a GPU job on AWS Batch.

The company in our story is KodeFood, a fast-food delivery app. Millions of people open it every day. Behind that screen sit more than two thousand vendors, and more join all the time. Each vendor needs menu photos. Those pictures are how customers decide what to tap.

Photos do not arrive perfect. A vendor uploads what they have — a clear plate of food, or a selfie, a logo, a random phone shot. KodeFood still has to show a catalog customers trust. So the platform’s job is broader than “store an image.” It turns messy uploads into a short description and a clear accepted or rejected status.

What we build is similar — not the same — to how real delivery platforms treat menu photos as product quality. DoorDash has written publicly about Drive photo quality in that spirit. A link for that article sits under Further reading if you want it later. Our path is a teaching-sized version: messy uploads in, usable catalog signals out.

That is the thread for every section. Photos in. Captions and decisions out. A GPU in the middle, because looking at images at scale is not ordinary CPU work.

Next we look hard at the image problem at scale — why manual review fails, and why KodeFood needs an automated path.

---

## Further reading (not spoken)

- https://about.doordash.com/en-us/news/doordash-drive-photo — how delivery platforms treat menu and storefront imagery as product quality, not decoration
- https://aws.amazon.com/batch/ — the service we will use later to run the GPU work on demand
