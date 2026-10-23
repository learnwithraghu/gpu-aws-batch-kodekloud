# Video 003 — CPU vs GPU: Why We Need Both

**Section:** 002 — GPU Fundamentals: From Silicon to Cloud
**Lecture#:** 003
**Sheet title:** CPU vs GPU: Why We Need Both
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 002-003-cpu-vs-gpu--why-we-need-both

---

If a GPU is so much faster at neural network math, why can’t we run our entire KodeFood job on a GPU alone?

Because a real production job is never pure math.

Think about everything our container has to do around the model. It starts a process, reads configuration, lists objects in S3, downloads JPEG files over the network, decodes image bytes, checks whether the generated caption looks like food, and writes a final CSV back to storage.

None of that is parallel matrix math. That is control flow, networking, file handling, and branching logic.

That is where the CPU stays in charge. You can think of the CPU as the orchestrator on the host. It handles operating system calls, network I/O, and sequential decisions, then prepares clean batches of image tensors and hands them across to the GPU for the heavy forward pass.

This split is one of the most practical debugging habits in production ML. When a GPU job is slow, inexperienced teams immediately blame the model. Experienced platform teams ask first: is the GPU actually working, or is it sitting idle waiting for the CPU to download and decode images?

Uber’s Michelangelo team has written about this exact boundary in production pipelines: data movement and preprocessing have very different bottlenecks from accelerator execution.

Let’s make one prediction. If you put slow, single-threaded S3 downloads inside a loop on an expensive GPU machine, you pay GPU prices while the CPU does basic network work.

So CPU and GPU are partners, not replacements. The CPU moves data and makes decisions; the GPU crunches the tensors.

Next, let’s open up the GPU itself and see what hardware sits inside the chip—and why GPU memory is the boundary you will hit first.

---

## Further reading (not spoken)

- [NVIDIA Developer Blog: CUDA Refresher — The CUDA Programming Model](https://developer.nvidia.com/blog/cuda-refresher-cuda-programming-model/) — how host CPU and device GPU split orchestration and parallel kernels
- [Uber Engineering: Michelangelo Machine Learning Platform](https://www.uber.com/blog/michelangelo-machine-learning-platform/) — separating data movement and compute execution in production ML systems
