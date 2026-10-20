# Video 001 — Why GPUs? From Graphics Hardware to AI Inference
**Section:** 002 — Understanding GPUs and AWS Batch
**Lecture#:** 001
**Sheet title:** Why GPUs? From Graphics Hardware to AI Inference
**Type:** Video
**Runtime target:** ~3 minutes
**Topic code:** 002-001-why-gpus?-from-graphics-hardwa

---

KodeFood will run its own caption model. To understand why that job asks for a GPU, let’s step back before neural networks.

A screen is a grid of pixels. Each frame in a game, film, or 3D model needs millions of similar color and geometry calculations at nearly the same time so motion stays smooth. A general-purpose CPU is built for flexible logic and branching decisions across a few powerful cores. A GPU takes a different approach: thousands of smaller cores that perform the same math across many elements together.

Now connect that hardware to our menu photos. Our job is not training a new model for every vendor. Training updates model weights over long runs. Our job performs inference. BLIP is already trained; it receives each photo, emits a short caption, and Python checks for food-like words to mark the row accepted or rejected.

Inside that caption step, each image becomes a tensor: height, width, and color channels represented as numbers. Model layers repeatedly multiply, add, and reduce those values. The parallel hardware once built to shade millions of pixels is a natural fit for that dense matrix math.

A CPU can process a folder of thirty photos, but it works through those layers slowly. A GPU runs the operations in parallel and finishes the folder in a short burst. Netflix-style recommendation pipelines use a similar pattern: run the heavy model scoring in a dedicated batch step, then let the product read the prepared output later.

Notice what we do not need. We do not need an always-on GPU endpoint waiting for clicks. We need GPU compute while a vendor folder is being processed, and then we want that capacity to return toward zero.

Next, let’s look inside one job and see what stays on the CPU, what moves to the GPU, and why GPU memory shapes how many photos we process at once.

---

## Further reading (not spoken)

- https://developer.nvidia.com/cuda-zone — NVIDIA’s overview of GPU computing beyond graphics
- https://huggingface.co/docs/transformers/tasks/image_captioning — image captioning as an inference task
- https://netflixtechblog.com/netflix-recommendations-beyond-the-5-stars-part-1-55838468f429 — industry example of offline batch scoring behind a consumer product
