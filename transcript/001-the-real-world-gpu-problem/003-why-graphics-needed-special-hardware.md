# Video 003 — Why graphics needed special hardware in the first place
**Section:** 001 — The Real-World GPU Problem
**Lecture#:** 003
**Sheet title:** Why graphics needed special hardware in the first place (drawing millions of pixels, fast)
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 001-003-why-graphics-needed-special-ha

---

KodeFood will run its own caption model. To understand the hardware choice, let’s step back before neural networks.

A screen is a grid of pixels. Each frame in a game, film, or 3D model may need millions of similar color calculations at nearly the same time. That is how motion stays smooth.

A general-purpose CPU is excellent at flexible logic and branching decisions. A GPU takes a different approach. It has thousands of smaller cores that can perform many similar operations together. Early GPUs used that design to shade pixels and transform geometry.

Now notice the connection to our job. A caption model receives an image as a tensor: height, width, and color channels represented as numbers. Its layers repeatedly multiply, add, and reduce those values. The parallel hardware that once focused on drawing frames is also well suited to this matrix math.

You do not need the full history of CUDA here. Keep one mental model: when the work is the same math across many elements, a GPU is a strong fit. When the work is a sequence of varied decisions and branches, the CPU usually stays in charge.

We now have the hardware idea. Next, let’s apply it directly to KodeFood’s caption-and-filter job and ask why a larger CPU box is not our first choice.

---

## Further reading (not spoken)

- https://developer.nvidia.com/cuda-zone — NVIDIA’s overview of GPU computing beyond games
- https://en.wikipedia.org/wiki/Graphics_processing_unit — concise history of GPUs as parallel processors for pixels, then general compute
