# Video 004 — Why GPUs for This Workload?
**Section:** 001 — The Real-World GPU Problem
**Lecture#:** 004
**Sheet title:** Why GPUs for This Workload?
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 001-004-why-gpus-for-this-workload?

---

We’ve traced the GPU from pixel work to parallel math. Now let’s apply that model to this KodeFood job.

The application is not training a new model for every vendor. Training would update model weights from labeled data, using optimizers over long runs. Our job performs inference. BLIP is already trained. It looks at each photo and emits a short caption. Then Python checks for food-like words and marks the row accepted or rejected.

The caption step contains the heavy matrix math. Each image becomes a grid of numbers that passes through many model layers. A CPU can process a folder of thirty photos, but it does the work slowly. A GPU runs many of those operations in parallel and finishes the folder in a shorter burst.

Also notice what we do not need. We do not need an always-on GPU endpoint. We need GPU capacity while a folder is being processed, then we want that capacity to fall back toward zero. That is the shape of on-demand batch inference.

The failure mode depends on where we run. On a local machine, CPU fallback makes captioning—not S3 listing or CSV writing—the bottleneck. In our Batch design, the job requests a GPU. If no GPU capacity is available, the job remains unplaced and the caption step never starts. That distinction will help us separate application logic from compute problems later.

So the GPU has a narrow, important role: accelerate the model’s vision math. Next, let’s trace one image folder all the way to the CSV KodeFood reads.

---

## Further reading (not spoken)

- https://pytorch.org/tutorials/beginner/former_torchies/parallelism_tutorial.html — how deep learning frameworks think about parallel compute
- https://netflixtechblog.com/netflix-recommendations-beyond-the-5-stars-part-1-55838468f429 — classic industry case of large-scale model scoring behind a consumer product
- https://huggingface.co/docs/transformers/tasks/image_captioning — image captioning as an inference task
