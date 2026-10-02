# Video 002 — Ideas to solve the problem: LLM vs Selfhosted application
**Section:** 001 — The Real-World GPU Problem
**Lecture#:** 002
**Sheet title:** Ideas to solve the problem : LLM vs Selfhosted application
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 001-002-ideas-to-solve-the-problem---l

---

We have a folder of vendor photos and need captions plus accept-or-reject decisions. There are two reasonable ways to get those captions.

The first is a hosted language or vision API. Send an image, receive a sentence, and keep the integration small. There is no GPU fleet to operate. For ten occasional photos, that can be a good fit.

Now change the scale to thousands of images a day. We need to account for per-image pricing, rate limits, network round trips, data crossing into another endpoint, and the provider’s latency and availability. None of those make hosted APIs wrong. They are simply tradeoffs we should name.

The second option is to self-host a finished caption model such as BLIP. We run it on our images and keep the accept-or-reject rule in Python. That gives us control over batching, the CSV contract, and where the image bytes travel. In return, we need a container that can use a GPU and somewhere to run it.

For this KodeFood job, we’ll use the self-hosted path. The workload is batch inference with a clear beginning and end. A vendor folder arrives. We process it, write `descriptions.csv`, and release the expensive capacity.

That leaves a useful question: why does the self-hosted path need special hardware? Next, we’ll trace why image work moved beyond ordinary CPU processing in the first place.

---

## Further reading (not spoken)

- https://huggingface.co/Salesforce/blip-image-captioning-base — the class of caption model our self-hosted path will use
- https://platform.openai.com/docs/guides/images-vision — example of a hosted vision API path, useful to contrast with batch self-hosting
- https://aws.amazon.com/what-is/inference/ — AWS overview of inference as “run a finished model,” which is our mode
