# Video 000 — What Is a GPU, Really?

**Section:** 002 — GPU Fundamentals: From Silicon to Cloud
**Lecture#:** 000
**Sheet title:** What Is a GPU, Really?
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 002-000-what-is-a-gpu--really?

---

We know KodeFood needs to inspect thousands of vendor menu photos without waiting on a human review queue. Before we touch AWS or containers, let’s ask a basic question: what is a GPU, really, and why does this kind of work need one?

The name stands for Graphics Processing Unit, which makes it sound like hardware built only for screens and games. In practice, a modern GPU is a massively parallel throughput processor.

Think about the difference between two styles of work. Some work is a chain of complicated decisions: check a condition, call an API, handle an error, and branch to the next step. Other work is the exact same arithmetic repeated millions of times across a giant grid of numbers.

A regular CPU is built for that first style. It has a small number of fast, flexible cores that switch tasks quickly. A GPU is built for the second style. It packs thousands of smaller execution units onto one chip so it can apply the same math to thousands of values at the same time.

Now look at a dish photo uploaded by a KodeFood vendor. To a computer, that photo is not a picture of noodles. It is a grid of millions of pixel values. Running a vision model means multiplying and adding those numbers across layer after layer.

Let’s make one prediction. If you hand a thousand identical math operations to a chip built for sequential logic, it works through them carefully, one small group at a time. Hand that same grid to a GPU, and it sweeps across the array in parallel.

So strip away the gaming label. A GPU is an engine for dense, uniform math at scale.

Next, let’s step back and see how hardware originally designed to draw pixels evolved into the processor behind modern AI.

---

## Further reading (not spoken)

- [NVIDIA: What Is a GPU?](https://www.nvidia.com/en-us/Glossary/gpu/) — core definition of graphics and parallel throughput processors
- [AWS: What Is a GPU?](https://aws.amazon.com/what-is/gpu/) — how cloud providers frame GPU accelerators for compute and AI workloads
