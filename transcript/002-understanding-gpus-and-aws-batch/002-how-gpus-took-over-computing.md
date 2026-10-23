# Video 002 — How GPUs Took Over Computing

**Section:** 002 — GPU Fundamentals: From Silicon to Cloud
**Lecture#:** 002
**Sheet title:** How GPUs Took Over Computing
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 002-002-how-gpus-took-over-computing

---

Once GPUs opened up to general math, why didn’t they stay a niche tool for physics labs? How did they end up at the center of almost every modern cloud data center?

Two trends collided at the same time.

First, traditional CPU scaling hit a wall. For decades, chips got faster simply by raising clock speeds. Eventually power and heat made that harder, so computing shifted toward parallelism: getting more done per clock cycle rather than just making a single core spin faster.

Second, deep learning arrived with an appetite for matrix multiplication that matched GPU hardware almost perfectly. When AlexNet won the ImageNet competition in 2012 using GPUs, it proved that training neural networks on parallel processors was not just slightly faster. It made models practical that were previously too slow to train at all.

Soon the workload expanded beyond research labs. Recommendation engines, fraud detection, speech recognition, and computer vision all turned out to rely on the same dense linear algebra.

Netflix’s engineering writing on recommendation and media pipelines reflects this shift: heavy model scoring moved onto dedicated accelerator stages, while product services read the prepared results.

Notice what changed for infrastructure teams. A GPU was no longer a workstation card plugged under someone’s desk. It became a rack-scale data-center resource that companies schedule, share, and guard carefully because of its cost.

When KodeFood runs a vision model over vendor dish photos, it is riding that exact wave: using data-center accelerators for repeatable matrix math.

Even so, a GPU server still has a CPU inside it. Next, let’s look at why we still need both processors working together in every real job.

---

## Further reading (not spoken)

- [Communications of the ACM: ImageNet Classification with Deep Convolutional Neural Networks](https://dl.acm.org/doi/10.1145/3065386) — the AlexNet milestone that accelerated GPU adoption in AI
- [Netflix TechBlog: Recommendations Beyond the 5 Stars](https://netflixtechblog.com/netflix-recommendations-beyond-the-5-stars-part-1-55838468f429) — how large consumer platforms pair heavy offline scoring with fast product reads
