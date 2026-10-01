# Video 004 — Why GPUs for This Workload?
**Section:** 001 — The Real-World GPU Problem
**Lecture#:** 004
**Sheet title:** Why GPUs for This Workload?
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 001-004-why-gpus-for-this-workload?

---

We just traced GPUs from drawing pixels to running parallel math. Now ask the sharper question: why does *this* KodeFood job need one?

Our application does not train a new model on each vendor’s menu. Training would update weights from labeled data, with optimizers and long runs. We do inference. A finished caption model — BLIP in our repo — looks at each photo and emits a short sentence. Then a few lines of Python check for food-like words and mark accepted or rejected.

Under that caption call sits matrix math. Each image becomes a large grid of numbers. The model pushes those numbers through many layers. A CPU can finish a folder of thirty photos eventually. A GPU finishes the same folder in one short burst because it runs those parallel operations together. For KodeFood, that difference is the difference between a snappy catalog refresh and a crawl.

Also notice what we are *not* buying. We are not renting an always-on GPU chat endpoint. We want a machine for the minutes a folder is processing, then we want capacity to fall back toward zero. That shape — on-demand batch inference — is why GPUs plus a scheduler matter more than “any cloud VM.”

Companies that ship visual search, moderation, or recommendations make the same distinction: train rarely, infer often, GPUs where the tensor work lives. Netflix’s classic recommendations writing is a different product than menu photos — but the hardware lesson rhymes. Further reading has that Tech Blog piece if you want the longer story.

That's it here for why this workload wants a GPU: vision math is the same family of parallel work graphics chips were built for. Next we walk the end-to-end flow from one image folder to the CSV KodeFood actually reads.

---

## Further reading (not spoken)

- https://pytorch.org/tutorials/beginner/former_torchies/parallelism_tutorial.html — how deep learning frameworks think about parallel compute
- https://netflixtechblog.com/netflix-recommendations-beyond-the-5-stars-part-1-55838468f429 — classic industry case of large-scale model scoring behind a consumer product
- https://huggingface.co/docs/transformers/tasks/image_captioning — image captioning as an inference task
