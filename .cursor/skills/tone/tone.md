# Reference & Examples for `tone` Skill (`tone.md`)

This reference accompanies [`SKILL.md`](SKILL.md) with concrete patterns and before/after examples drawn from the repository's `transcript/` directory.

---

## 1. Spoken Phrasing Shifts (Documentation vs. Teleprompter)

| Avoid (Documentation / Monotone / Code-Heavy) | Prefer (Teleprompter / Question-Led / Senior Engineer Voice) |
|---|---|
| *"Submit to `gpu-teaching-gpu-smoke-queue-spot` using `gpu-teaching-caption-job` with overrides `IMAGE_PREFIX` and `python /app/describe_items.py`."* | *"Now we tell Batch which vendor folder to process, and Batch figures out where that job should run."* |
| *"According to DoorDash's blog post at URL X, they solved this exact problem with GPU batch jobs."* | *"That is not just a teaching problem. DoorDash has also written publicly about treating menu and storefront imagery as part of product quality, not as decoration around the product."* |
| *"In `describe_items.py`, line 42 calls `processor(images=batch)` and moves tensors to `cuda:0`."* | *"Inside that caption step, each image becomes a grid of numbers that passes through the model layers in parallel on the GPU."* |
| *"That's it here for IAM roles. In the next video we will cover networking."* | *"So the real lesson here is not memorizing role names. It is learning to separate orchestrator permissions, host permissions, and application permissions. Next, we pair permission with connectivity and look at the network path a Batch GPU job still needs in order to work."* |

---

## 2. Industry Anchor Mapping (Use in ~50% of Video Scripts)

Only name a company when the concept matches the linked `Further reading` source, and never overstate what the public source proves:

- **Product & catalog quality (Sections 001, 003):** **DoorDash** — menu and storefront imagery as product quality and conversion trust, turning messy vendor uploads into structured catalog signals.
- **Scaling & ML platform boundaries (Sections 001, 003, 007):** **Uber (Michelangelo)** — when human review turns into a systems design problem; separating data movement from expensive model compute; keeping units of work small and restartable.
- **Offline batch inference vs. real-time (Sections 002, 007):** **Netflix** — running heavy model scoring in a dedicated offline batch step so the customer-facing product reads prepared output quickly.
- **Storage contracts & lineage (Section 004):** **Airbnb (Bighead)** — separating input/output storage concerns cleanly so permissions, lineage, and debugging remain easy to reason about.
- **Hosted API vs. self-hosted tradeoff (Section 002):** **OpenAI-style vision APIs vs. self-hosted BLIP** — renting intelligence per request vs. operating a repeatable batch container with predictable data boundaries.

---

## 3. Canonical Examples from This Repo

### Example A — Opening with "Why" and Company Debugging (`003/001`)

```markdown
Why separate storage logic from GPU processing at all?

Because they are different kinds of work, and companies debug them differently.

One side of the application is about data movement. Which images are we reading? Can we access them? Can we produce and store the output correctly? The other side is about model execution. Can the GPU workload start? Can the model process the images? Can it generate useful results within the available memory and time?

Those two concerns often fail for very different reasons. A missing object, wrong prefix, or write problem is not the same kind of issue as a GPU memory problem or an inference failure. If you mix them together mentally, every failure starts to look the same.

That is why this separation is so helpful. It gives the team a clean first question when something breaks: is this a data-path problem, or is this a model-path problem?
```

### Example B — Operational State & Symptom Thinking (`006/006`)

```markdown
`RUNNABLE` sounds encouraging, but it often frustrates beginners.

The important meaning is this: the job is ready in theory, but Batch still has nowhere to place it.

That also means the application is not running yet. No container has started. So this is not the moment to begin blaming the code or searching for application logs.

In real teams, `RUNNABLE` usually points to one of a few operational questions. Is GPU capacity actually available? Is the chosen purchase model currently placeable? Is the account allowed to launch that kind of instance? Or did the job ask for a resource profile that does not fit the target machine?

Notice what all of those have in common: they are placement questions, not application questions.
```

### Example C — Section 008 Global Context Connected Back to KodeFood (`008/000`)

```markdown
Batch, ECS, EKS, and SageMaker all depend on the same thing: an available accelerator. When the KodeFood job remains RUNNABLE in Tokyo, a small application is meeting a global infrastructure constraint.
...
KodeFood shows the practical response. It uses finite inference jobs, prefers Spot capacity, and scales toward zero. Captioning vendor dishes does not need a supercluster. It needs a small amount of reliable GPU time, followed by no GPU bill at all.

Treat accelerator capacity as a dependency, not an assumption. Next we follow the supply chain from chip design to the cloud rack that runs the Batch job.
```
