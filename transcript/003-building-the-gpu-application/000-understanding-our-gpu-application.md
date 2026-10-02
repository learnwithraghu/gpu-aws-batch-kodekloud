# Video 000 — Understanding Our GPU Application

**Section:** 003 — Building the GPU Application
**Lecture#:** 000
**Sheet title:** Understanding Our GPU Application
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 003-000-understanding-our-gpu-applicat

---

You have seen the AWS Batch GPU architecture: queues, compute environments, and job definitions. Now let’s put the real KodeFood job in the middle. What command runs when a GPU machine starts?

Batch starts one Python entrypoint: `python /app/describe_items.py`. That script loads the BLIP model and reads one vendor photo folder. It generates captions, marks each photo accepted or rejected, and produces one catalog CSV.

Notice the execution path. The job definition points to a container image. That image contains `/app/describe_items.py`. When GPU capacity is ready, the container starts and runs the script. This is a finite batch job. It is not a service or an interactive notebook.

For KodeFood, the contract is deliberately small: one vendor folder in, one `descriptions.csv` out. A simple food-word rule checks each generated caption.

The file on your laptop is only source code. Batch runs the copy baked into the image at `/app/`. If you edit the script but do not rebuild and push the image, the next job still runs the old code. That symptom belongs to the image delivery path, not to the GPU.

Keep this mental model: Batch schedules the capacity, and `describe_items.py` performs the work. S3 helpers, Docker, and CUDA support that entrypoint.

Next, we will separate storage operations from model processing. That split will give us a clear first place to look when this job fails.

---

## Further reading (not spoken)

- [Salesforce BLIP model card (Hugging Face)](https://huggingface.co/Salesforce/blip-image-captioning-base) — the caption model this course loads
- [AWS Batch: Job definitions](https://docs.aws.amazon.com/batch/latest/userguide/job_definitions.html) — where the container command and image are declared
- [DoorDash Engineering Blog](https://doordash.engineering/blog/) — marketplace engineering context for catalog and quality systems
