# Video 001 — Separating Storage Logic from GPU Processing

**Section:** 004 — Building the GPU Application
**Lecture#:** 001
**Sheet title:** Separating Storage Logic from GPU Processing
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 004-001-separating-storage-logic-from-

---

Why separate storage logic from GPU processing at all?

Because they are different kinds of work, and companies debug them differently.

One side of the application is about data movement. Which images are we reading? Can we access them? Can we produce and store the output correctly? The other side is about model execution. Can the GPU workload start? Can the model process the images? Can it generate useful results within the available memory and time?

Those two concerns often fail for very different reasons. A missing object, wrong prefix, or write problem is not the same kind of issue as a GPU memory problem or an inference failure. If you mix them together mentally, every failure starts to look the same.

That is why this separation is so helpful. It gives the team a clean first question when something breaks: is this a data-path problem, or is this a model-path problem?

Uber’s Michelangelo is a good mental reference here. Keep the boundaries visible. Let one layer handle storage and movement of data. Let another layer handle the expensive compute. The result is easier testing, easier debugging, and clearer ownership.

So before we even talk about the model itself, we already have a useful operating principle: separate the work that moves the data from the work that reasons over the data.

Next, we focus on the GPU side and see what inference actually means in this application.

---

## Further reading (not spoken)

- [PyTorch: Saving and loading models](https://pytorch.org/tutorials/beginner/saving_loading_models.html) — `eval()` and inference vs training mindset
- [AWS S3: Listing object keys](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ListingKeysUsingAPIs.html) — how prefix listing finds work
- [Uber Engineering: Michelangelo](https://www.uber.com/blog/michelangelo-machine-learning-platform/) — separating data and ML platform concerns at scale
