# Video 005 — From Images to Captions and Accept/Reject Decisions
**Section:** 001 — The Real-World GPU Problem
**Lecture#:** 005
**Sheet title:** From Images to Captions and Accept/Reject Decisions
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 001-005-from-images-to-captions-and-ac

---

We know why a GPU helps caption photos. Let’s trace one vendor folder through the product, end to end.

Input lives in object storage under a simple prefix: `images/<stem>/` inside the images bucket. About twenty-five to thirty jpg, jpeg, or png files for that batch. Output is equally strict: `descriptions/<stem>/descriptions.csv` in the CSV bucket. One folder in. One catalog file out.

Inside the job, two stories share one process. Storage code lists the prefix, downloads bytes, and later writes the CSV. GPU code loads BLIP, describes photos in small groups — eight at a time by default so they fit in GPU memory — and returns sentences. Then `photo_status` looks at each caption. If food-like words appear, the row is accepted. If the caption sounds like a car, a selfie, or a logo, it is rejected. Rejected rows stay in the file so the reason is visible. Accepted rows feed the menu text.

The CSV columns are the contract the app trusts: the image URI, the item description, and the photo status. KodeFood does not open the raw folder to invent titles at request time. It reads this file. If the CSV is wrong, the product is wrong — even if the GPU “ran fine.”

Hold that picture. You now have the real-world problem, the self-hosted caption choice, and the accept-or-reject outcome. What still feels fuzzy is the hardware split itself: what actually changes when this work runs on a CPU versus a GPU?

That’s the door into section two. Next we compare CPU and GPU for this workload — not as slogans, but as what changes for memory, speed, and how we batch photos.

---

## Further reading (not spoken)

- https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-folders.html — S3 prefixes as the layout contract for inputs and outputs
- https://huggingface.co/Salesforce/blip-image-captioning-base — the caption model behind the descriptions in our pipeline
