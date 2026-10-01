# Video 003 — How GPU Inference Works Inside the Application

**Section:** 003 — Building the GPU Application
**Lecture#:** 003
**Sheet title:** How GPU Inference Works Inside the Application
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 003-003-how-gpu-inference-works-inside

---

Storage is in `photos.py`. The GPU story lives in `describe_items.py`. Let’s trace what happens after the model loads.

First the job picks a device: `cuda` when a GPU is present, otherwise `cpu`. On Batch with a healthy `g4dn`, you want Device: cuda in the logs. Then it loads Salesforce’s BLIP image-captioning base model and moves the weights onto that device.

Right after load, the code calls `model.eval()`. That one line matters. Some layers behave differently while training — dropout is the classic example. Eval mode tells PyTorch: we are describing photos, not updating weights. There is no optimizer and no loss. We are generating text, not teaching the model new dishes.

For each small group of images, a processor turns pixels and a short prompt into tensors on the GPU. Then `model.generate` runs under `torch.no_grad()`. No grad skips the backprop graph. That saves memory and matches the product: captions in a CSV, not a training run.

The prompt is a short photography-style prefix. Generate uses a few beams, a short token cap, and a repetition penalty so captions stay concise. Prompt plus generate settings produce the sentence that lands in the catalog.

After that, a small Python check looks for food-like words. Match means accepted; otherwise rejected. That rule is not a second model, and it does not prove the dish matches the menu. It catches obvious bad uploads — a selfie, a car, a logo — so KodeFood can prefer food-looking photos.

You might wonder: if inference is one forward generate pass, why not send all thirty photos at once? That question is about GPU memory, and it is exactly where we go next — micro-batching.

---

## Further reading (not spoken)

- [BLIP: Bootstrapping Language-Image Pre-training (paper)](https://arxiv.org/abs/2201.12086) — original BLIP work from Salesforce Research
- [PyTorch: torch.no_grad](https://pytorch.org/docs/stable/generated/torch.no_grad.html) — why inference disables gradient tracking
- [Hugging Face: Generation strategies](https://huggingface.co/docs/transformers/generation_strategies) — beams, length limits, and decoding choices
