# Video 001 — The KodeFood Problem: Processing Vendor Images at Scale
**Section:** 001 — The Real-World GPU Problem
**Lecture#:** 001
**Sheet title:** The KodeFood Problem: Processing Vendor Images at Scale
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 001-001-the-kodefood-problem--processi

---

We’ve met KodeFood and its vendor menus. Now let’s put some numbers behind the problem.

One vendor uploads about twenty-five to thirty dish photos. A person could review that folder. But multiply it by hundreds of new and updating vendors in a week. Now thousands of images need two quick answers: does this belong on a food menu, and what short description should go with it?

Manual review starts to fail at that scale. The queue grows overnight. New vendors wait. Bad photos can reach the live menu, while good photos sit unpublished.

Notice that KodeFood does not need an art critique. It needs a practical result for each image: one short sentence, then accepted if the caption looks food-like, or rejected if it does not. Rejected rows remain in the catalog so operations can inspect them.

Let’s make one prediction. If image arrival outpaces human review, the backlog must grow even when every reviewer is working correctly. That tells us this is a scaling problem, not a training problem for the review team.

So the contract is clear. One vendor folder goes in. One CSV of captions and accept-or-reject decisions comes out. We run it on demand, without leaving expensive machines idle when the queue is empty.

With the problem bounded, we can compare two solutions: call a hosted model for each image, or run our own caption model.

---

## Further reading (not spoken)

- https://www.uber.com/blog/scaling-ml-platform/ — Uber on scaling ML platforms behind product features that touch huge volumes of data
- https://cloud.google.com/blog/products/ai-machine-learning/reducing-the-need-for-manual-data-labeling — why high-volume labeling shifts from pure human review toward automation
