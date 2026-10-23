# Video 000 — Understanding Our GPU Application

**Section:** 004 — Building the GPU Application
**Lecture#:** 000
**Sheet title:** Understanding Our GPU Application
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 004-000-understanding-our-gpu-applicat

---

We have talked about GPUs and how Batch schedules finite jobs. Now let’s talk about the actual application that sits in the middle.

What is this job really doing for KodeFood?

It takes one vendor’s folder of photos, generates short captions, applies a simple acceptance check, and produces one structured catalog file. That is the whole business outcome. Not a long-running service. Not an interactive tool. One finite unit of work with one finite result.

That small contract is important. In a real company, a system becomes easier to operate when each job has a clear beginning, a clear end, and a clear output. One folder in. One result out.

DoorDash’s engineering material points at the same broader concern: turning messy marketplace inputs into reliable catalog-quality outputs.

It also tells us how to think about AWS Batch. Batch is not the application itself. Batch is the scheduler. Its job is to provide the environment and run the workload. The application is the logic that turns raw images into useful catalog data.

This distinction matters when things go wrong. Sometimes the platform fails to place or start the job. Sometimes the application runs but produces the wrong outcome. Those are different classes of problems, and good teams separate them early.

So keep the mental model simple: Batch decides where and when the work runs, and the GPU application decides what business result gets produced.

Next, we break that application into two responsibilities so the failure path becomes easier to reason about.

---

## Further reading (not spoken)

- [Salesforce BLIP model card (Hugging Face)](https://huggingface.co/Salesforce/blip-image-captioning-base) — the caption model this course loads
- [AWS Batch: Job definitions](https://docs.aws.amazon.com/batch/latest/userguide/job_definitions.html) — where the container command and image are declared
- [DoorDash Engineering Blog](https://doordash.engineering/blog/) — marketplace engineering context for catalog and quality systems
