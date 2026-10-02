# Video 005 — From Images to Captions and Accept/Reject Decisions
**Section:** 001 — The Real-World GPU Problem
**Lecture#:** 005
**Sheet title:** From Images to Captions and Accept/Reject Decisions
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 001-005-from-images-to-captions-and-ac

---

We know why a GPU helps with captioning. Now let’s trace one vendor folder through the full job.

The input is under `images/<stem>/` in the images bucket. Each batch contains about twenty-five to thirty jpg, jpeg, or png files. The output has an equally strict location: `descriptions/<stem>/descriptions.csv` in the CSV bucket. One folder in, one catalog file out.

Inside the job, storage work and model work share one process. The storage code lists the prefix, downloads image bytes, and later writes the CSV. The GPU code loads BLIP and describes photos in small groups. The default is eight at a time so the active batch fits in GPU memory.

Then `photo_status` checks each caption. Food-like words produce an accepted row. A caption that sounds like a car, selfie, or logo produces a rejected row. We keep rejected rows in the file so operations can inspect the result. Accepted rows supply the menu text.

The CSV is the product contract: image URI, item description, and photo status. KodeFood does not generate titles from the raw folder during a customer request. It reads this file. If this contract is wrong, the product is wrong even when the GPU job reports success.

We now have the end-to-end path. In section two, we’ll separate the CPU and GPU responsibilities and see how memory and batch size affect that path.

---

## Further reading (not spoken)

- https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-folders.html — S3 prefixes as the layout contract for inputs and outputs
- https://huggingface.co/Salesforce/blip-image-captioning-base — the caption model behind the descriptions in our pipeline
