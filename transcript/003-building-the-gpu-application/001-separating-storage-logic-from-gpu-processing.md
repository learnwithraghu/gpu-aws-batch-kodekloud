# Video 001 — Separating Storage Logic from GPU Processing

**Section:** 003 — Building the GPU Application
**Lecture#:** 001
**Sheet title:** Separating Storage Logic from GPU Processing
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 003-001-separating-storage-logic-from-

---

Batch runs `describe_items.py`, but the application has two clear responsibilities. Let’s trace them before we look at the model.

`photos.py` owns storage. It lists photo keys under an S3 prefix, downloads each object as an image, and writes the completed catalog CSV. It does not load a model or call CUDA. If the logs show an empty prefix, `AccessDenied`, or a failed CSV upload, start with this file and the S3 permissions.

`describe_items.py` owns the GPU path. It loads BLIP, runs inference in groups, and applies the food-word accept or reject rule. It calls `photos.py` to list, download, and save. Batch still starts one process in one container. Python imports connect the files.

This split gives us a useful diagnostic boundary. A wrong bucket or missing object is a data-path problem. Missing CUDA, an out-of-memory error, or invalid generation settings are model-path problems. Both can end with the same failed job status, so the log symptom tells you which layer to inspect.

Environment variables connect runtime data to the application. Bucket names and `IMAGE_PREFIX` arrive when we submit the job. The same image can process `images/sample` today and another vendor stem tomorrow. No rebuild is needed; only the override changes.

Keep storage and CSV handling on one side, and model execution on the other. In the next lesson, we will follow one photo through BLIP and see why this job performs inference rather than training.

---

## Further reading (not spoken)

- [PyTorch: Saving and loading models](https://pytorch.org/tutorials/beginner/saving_loading_models.html) — `eval()` and inference vs training mindset
- [AWS S3: Listing object keys](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ListingKeysUsingAPIs.html) — how prefix listing finds work
- [Uber Engineering: Michelangelo](https://www.uber.com/blog/michelangelo-machine-learning-platform/) — separating data and ML platform concerns at scale
