# Video 000 — Understanding Our GPU Application

**Section:** 003 — Building the GPU Application
**Lecture#:** 000
**Sheet title:** Understanding Our GPU Application
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 003-000-understanding-our-gpu-applicat

---

You just walked the AWS Batch GPU architecture — queues, compute environments, job definitions. So far that story had an empty center: what command actually runs when a GPU machine starts?

Now we build that application. For KodeFood, Batch does not start a mystery binary. It starts one Python entrypoint: `python /app/describe_items.py`. That file is the caption job. It loads the BLIP model, walks a vendor photo folder, writes captions, and marks each photo accepted or rejected for the menu.

Notice what that means for you as an engineer. The job definition points at a container image. The image contains `/app/describe_items.py`. When capacity appears, the container starts, that script runs, and the product outcome is one catalog CSV — not a long-lived service, not an interactive notebook.

Delivery marketplaces treat catalog quality the same way in spirit. What we build is similar to DoorDash’s public engineering story around catalog and quality — not a copy of their stack. One vendor folder in, one `descriptions.csv` out, food-word rule on the caption. Further reading has their engineering blog when you want that wider context.

The script on your laptop is only the source. After we push to Amazon ECR, Batch runs whatever was baked into the image at `/app/`. Edit locally and forget to rebuild, and the next job still runs yesterday’s code. Hold that idea — we will keep returning to it.

So the mental model is simple. Batch schedules GPU capacity. The application is `describe_items.py`. Everything else — S3 helpers, Docker, CUDA — exists to make that entrypoint succeed the same way every time.

Where does that leave storage? Captioning needs photos on the way in and a CSV on the way out. The next video splits that storage work from the GPU work so each piece stays readable.

---

## Further reading (not spoken)

- [Salesforce BLIP model card (Hugging Face)](https://huggingface.co/Salesforce/blip-image-captioning-base) — the caption model this course loads
- [AWS Batch: Job definitions](https://docs.aws.amazon.com/batch/latest/userguide/job_definitions.html) — where the container command and image are declared
- [DoorDash Engineering Blog](https://doordash.engineering/blog/) — marketplace engineering context for catalog and quality systems
