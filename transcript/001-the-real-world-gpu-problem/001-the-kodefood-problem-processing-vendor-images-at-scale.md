# Video 001 — The KodeFood Problem: Processing Vendor Images at Scale
**Section:** 001 — The Real-World GPU Problem
**Lecture#:** 001
**Sheet title:** The KodeFood Problem: Processing Vendor Images at Scale
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 001-001-the-kodefood-problem--processi

---

We just met KodeFood and its vendor menus. Now let’s put numbers on the pain.

Imagine one vendor onboarding day. That kitchen uploads a folder of about twenty-five to thirty dish photos. That alone is manageable for a human. Now multiply by hundreds of new and updating vendors in a week. Suddenly you are staring at thousands of images that all need a quick judgment: is this actually food that belongs on a menu, and what short text should sit next to it?

Manual review does not scale here. A reviewer can open tabs for a while. Then the queue grows overnight. New vendors wait. Bad photos slip into the live menu. Good photos sit unpublished.

Notice what KodeFood needs from each photo. Not a perfect critique. A practical check: one short sentence, then accepted if it looks food-like, rejected if not. Rejected rows stay in the catalog file so operations can see why.

That pattern shows up beyond our fictional app. Uber’s writing on scaling ML platforms describes the same pressure: huge volumes cannot wait on humans labeling every row. We are not copying Uber — we are solving a smaller, similar shape. Photos in storage, automation labels them, the app reads structured results. Further reading has that Uber piece if you want their framing.

So the problem statement is sharp. One vendor folder in. One CSV of captions and accept-or-reject decisions out. Do that on demand, without leaving expensive machines running when the queue is empty.

That's it here for the scale problem: humans cannot open every photo, and the catalog still needs trust. Next: call a hosted model per image, or run our own caption model as a self-hosted application?

---

## Further reading (not spoken)

- https://www.uber.com/blog/scaling-ml-platform/ — Uber on scaling ML platforms behind product features that touch huge volumes of data
- https://cloud.google.com/blog/products/ai-machine-learning/reducing-the-need-for-manual-data-labeling — why high-volume labeling shifts from pure human review toward automation
