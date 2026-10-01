# Video 002 — Ideas to solve the problem: LLM vs Selfhosted application
**Section:** 001 — The Real-World GPU Problem
**Lecture#:** 002
**Sheet title:** Ideas to solve the problem : LLM vs Selfhosted application
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 001-002-ideas-to-solve-the-problem---l

---

We framed the need: folders of vendor photos in, captions and accept-or-reject out. So how do we get those captions?

Idea one is tempting. Call a hosted large language model or vision API for every image. You send the photo, get a sentence back, and write a few lines of glue code. No GPU fleet to manage. On a quiet Tuesday with ten photos, that feels elegant.

Now stretch it. Thousands of images a day. Per-image pricing. Rate limits. Network round trips. Data leaving your account into someone else’s endpoint. You also inherit their latency and their outage window. For a catalog pipeline that can wait a few minutes, an always-online chat-style API is often more machine than you need — and more cost than a short batch run.

Idea two is to self-host a caption model. Load a finished vision model such as BLIP, run it on your images, and keep the accept-or-reject rule in your own Python. You control the prompt, the batch size, the output CSV shape, and where the bytes live. The tradeoff is real: you need somewhere to run a GPU for those minutes, plus a container image that knows how to talk to that GPU.

For KodeFood in this course, we choose the self-hosted path. Not because APIs are wrong everywhere, but because our workload is batch inference with a clear start and end. Vendors drop folders. We process them. We write `descriptions.csv`. Then we want the expensive capacity to go away.

You might wonder why that second path keeps mentioning special hardware at all. Why can’t an ordinary server just “look” at the photos? That question is older than KodeFood. Next we go back to why graphics needed special hardware in the first place.

---

## Further reading (not spoken)

- https://huggingface.co/Salesforce/blip-image-captioning-base — the class of caption model our self-hosted path will use
- https://platform.openai.com/docs/guides/images-vision — example of a hosted vision API path, useful to contrast with batch self-hosting
- https://aws.amazon.com/what-is/inference/ — AWS overview of inference as “run a finished model,” which is our mode
