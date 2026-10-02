# Video 000 — The KodeFood Platform
**Section:** 001 — The Real-World GPU Problem
**Lecture#:** 000
**Sheet title:** The KodeFood Platfrom
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 001-000-the-kodefood-platfrom

---

Welcome to Building Production GPU Workloads on AWS.

We’re going to follow one product problem all the way into a GPU job on AWS Batch.

Our example company is KodeFood, a fast-food delivery app. Millions of people use it, and more than two thousand vendors supply its menus. Each vendor needs menu photos. Those photos help customers decide what to order.

But vendor uploads are messy. One folder may contain a clear plate of food, a selfie, a logo, or a random phone shot. KodeFood still needs a catalog customers can trust. So storing the image is only the first step. The platform must produce a short description and a clear accepted or rejected status.

We’ll build a teaching-sized version of that flow. Messy uploads go in. Usable catalog signals come out.

Keep that thread in mind through every section: photos in, captions and decisions out, with a GPU handling the image work in the middle.

Next, let’s put some scale behind the problem and see where manual review starts to break down.

---

## Further reading (not spoken)

- https://about.doordash.com/en-us/news/doordash-drive-photo — how delivery platforms treat menu and storefront imagery as product quality, not decoration
- https://aws.amazon.com/batch/ — the service we will use later to run the GPU work on demand
