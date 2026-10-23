# Video 003 — How GPU Inference Works Inside the Application

**Section:** 004 — Building the GPU Application
**Lecture#:** 003
**Sheet title:** How GPU Inference Works Inside the Application
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 004-003-how-gpu-inference-works-inside

---

Now let’s focus on the core GPU work: inference.

Inference means the model is not learning from the photos. It is using what it already knows to produce an output. In our case, that output is a caption for each image.

That distinction matters because many beginners hear "AI workload" and imagine training. But KodeFood is not training a food model here. It is running a ready-made model over incoming vendor photos so the business can get usable catalog signals quickly.

The application flow is conceptually simple. Images come in. The model interprets them. A caption is produced. Then a lightweight business rule turns that caption into a basic accept or reject decision.

This is a very realistic company pattern. The expensive model produces a rich output. Then a simpler business rule translates that output into a practical operational decision.

It is also why a GPU helps. The heavy part is not writing a row to a CSV. The heavy part is the model computation needed to understand image content fast enough to be useful at scale.

So when you think about inference in this course, do not picture a mysterious AI black box. Picture a production step that converts raw images into structured signals another system can act on.

Next, we ask the operational question that appears immediately after that: how many images should the GPU handle at one time?

---

## Further reading (not spoken)

- [BLIP: Bootstrapping Language-Image Pre-training (paper)](https://arxiv.org/abs/2201.12086) — original BLIP work from Salesforce Research
- [PyTorch: torch.no_grad](https://pytorch.org/docs/stable/generated/torch.no_grad.html) — why inference disables gradient tracking
- [Hugging Face: Generation strategies](https://huggingface.co/docs/transformers/generation_strategies) — beams, length limits, and decoding choices
