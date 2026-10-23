# Video 001 — From Pixels to Processors: A GPU History

**Section:** 002 — GPU Fundamentals: From Silicon to Cloud
**Lecture#:** 001
**Sheet title:** From Pixels to Processors: A GPU History
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 002-001-from-pixels-to-processors--a-g

---

Why did the chip that now captions KodeFood menu photos start out inside video game hardware?

Because three-dimensional graphics had a math problem that ordinary processors could not keep up with.

Think about what happens every time a game renders a single frame. The scene is built from triangles and textures, and the screen is a grid of millions of pixels. To keep motion smooth, the machine has to calculate lighting, position, and color for all those pixels dozens of times every second.

Early graphics chips were fixed-function pipelines. They did that specific pixel and triangle math very fast, and nothing else. You could not hand them an arbitrary program.

Then hardware engineers noticed something important. Developers wanted custom lighting and visual effects, so GPUs added programmable shaders. Instead of hard-wiring one formula in silicon, the chip let programmers run a small math routine across thousands of pixels in parallel.

Researchers outside gaming spotted the opportunity immediately. If a GPU can run custom math across millions of pixels, what stops us from disguising a physics simulation, a financial model, or a matrix multiplication as a texture of numbers?

That was the turning point. Once NVIDIA introduced CUDA in the mid-2000s, engineers no longer had to pretend their data was a 3D scene. They could send general arrays of numbers straight to those parallel cores.

So the history is a straight line: fixed pixel hardware became programmable shader processors, and programmable shaders became general-purpose parallel compute.

Next, let’s look at what happened once software could talk to those cores directly, and how GPUs took over modern computing.

---

## Further reading (not spoken)

- [NVIDIA Developer Blog: Reviewing the Origins of GPU Computing](https://developer.nvidia.com/blog/cuda-refresher-reviewing-the-origins-of-gpu-computing/) — evolution from fixed-function graphics pipelines to programmable parallel compute
- [IEEE Spectrum: How GPUs Came to Rule AI](https://spectrum.ieee.org/gpu-history) — historical path from 3D rendering chips to data-center accelerators
