# Video 001 — Separating Storage Logic from GPU Processing

**Section:** 003 — Building the GPU Application
**Lecture#:** 001
**Sheet title:** Separating Storage Logic from GPU Processing
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 003-001-separating-storage-logic-from-

---

We said Batch runs `describe_items.py`. Open that story one layer deeper and you will see two files, not one.

`photos.py` owns storage. It lists photo keys under an S3 prefix, downloads each object into an image, and writes the finished catalog CSV. There is no CUDA call in that file. No model load. No generate step. If listing fails, if IAM denies GetObject, if the CSV upload fails — you look here first.

`describe_items.py` owns the GPU path. It loads BLIP, runs inference in groups, applies the food-word accept or reject rule, and calls into `photos.py` for list, download, and save. Batch still starts one process. Imports connect the two files. The split is for humans reading the failure, not for two containers.

Why bother? Because production GPU jobs mix two failure modes that look the same from the outside: “the job failed.” One mode is data path — wrong bucket, empty prefix, AccessDenied. The other is model path — CUDA missing, out of memory, bad generate settings. When storage and GPU live in one tangled script, every red exit becomes a guessing game.

Real pipeline teams draw the same line. Uber’s Michelangelo platform wrote openly about keeping data pipelines apart from training and inference. We are borrowing that separation idea at course scale — not their platform. Keep I/O readable, keep the model readable. Further reading has the Michelangelo article if you want the original framing.

Environment variables glue the split together. Buckets and `IMAGE_PREFIX` arrive at submit time. The same image can caption `images/sample` today and another vendor stem tomorrow without a rebuild. Only the override changes.

That's it here for the split: S3 and CSV stay out of the GPU path. Next — how BLIP captions a photo, and why we never train in this job.

---

## Further reading (not spoken)

- [PyTorch: Saving and loading models](https://pytorch.org/tutorials/beginner/saving_loading_models.html) — `eval()` and inference vs training mindset
- [AWS S3: Listing object keys](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ListingKeysUsingAPIs.html) — how prefix listing finds work
- [Uber Engineering: Michelangelo](https://www.uber.com/blog/michelangelo-machine-learning-platform/) — separating data and ML platform concerns at scale
