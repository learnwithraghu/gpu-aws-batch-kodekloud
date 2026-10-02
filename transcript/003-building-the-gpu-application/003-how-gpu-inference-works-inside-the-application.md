# Video 003 — How GPU Inference Works Inside the Application

**Section:** 003 — Building the GPU Application
**Lecture#:** 003
**Sheet title:** How GPU Inference Works Inside the Application
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 003-003-how-gpu-inference-works-inside

---

Storage stays in `photos.py`. GPU processing lives in `describe_items.py`. Let’s trace one group of KodeFood photos after the model loads.

First, the job selects a device: `cuda` when a GPU is available, otherwise `cpu`. On a healthy Batch `g4dn` job, the logs should say Device: cuda. If they say cpu, inspect GPU exposure and the software stack before tuning the model. The job then loads Salesforce’s BLIP image-captioning base model and moves its weights to the selected device.

Next, the code calls `model.eval()`. Some layers, including dropout, behave differently during training, and eval mode switches them to inference behavior. The code has no optimizer or loss calculation, while `torch.no_grad()` in the next step disables gradient tracking.

The processor converts each small group of images and a short prompt into tensors on the GPU. Then `model.generate` runs inside `torch.no_grad()`. Disabling gradient tracking avoids building the backpropagation graph and reduces memory use. That is the right behavior for producing captions, not training a model.

Generation uses a photography-style prompt, a few beams, a short token limit, and a repetition penalty. Together, those settings shape the sentence written to the catalog.

Finally, a Python check looks for food-like words. A match is accepted; anything else is rejected. This rule does not verify that the dish matches the menu. It only filters obvious non-food uploads such as a selfie, car, or logo.

We now have the full inference path. The remaining question is how many photos should share one call to `model.generate`. That takes us to GPU micro-batching.

---

## Further reading (not spoken)

- [BLIP: Bootstrapping Language-Image Pre-training (paper)](https://arxiv.org/abs/2201.12086) — original BLIP work from Salesforce Research
- [PyTorch: torch.no_grad](https://pytorch.org/docs/stable/generated/torch.no_grad.html) — why inference disables gradient tracking
- [Hugging Face: Generation strategies](https://huggingface.co/docs/transformers/generation_strategies) — beams, length limits, and decoding choices
