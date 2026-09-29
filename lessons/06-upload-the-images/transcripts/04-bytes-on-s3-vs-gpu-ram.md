# Video 04 — Bytes on S3 versus GPU memory
**Type:** Theory
**Runtime target:** ~3 minutes

---

So, a few megabytes in S3 is not the same as GPU memory.

A few megabytes in S3 is the size of the file at rest. It is not the size of the work the GPU does. The job downloads the jpeg. photos.py opens those bytes and converts them to an RGB picture. That decoded picture is much larger than the file you uploaded. describe_items.py turns a group of those pictures into tensors on the device and runs the caption model. Peak memory follows the decoded group, not the sum of jpeg sizes in the bucket.

That is why BATCH_SIZE counts photos. The default is eight. Thirty photos become four passes, eight, then eight, then eight, then six. Each pass is one GPU forward. Sentences append to one list. At the end, one CSV is written with image_s3_uri, item_description, and photo_status. The groups are a memory tactic, not extra output files. Eight small photos and eight huge photos are both a batch of eight, and they do not cost the same device memory.

Eight photos at twelve megapixels can run out of GPU memory where eight at two megapixels succeed. Same count, same model, different decoded size. Later knobs are a smaller BATCH_SIZE, or a resize before the tensor is built. This lesson does not do that resize. Large files also take longer to download and longer for the CPU to decode. A job can look stuck in the download and still be healthy.

The instance is a g4dn.xlarge, one T4, loaded once for the whole folder. KodeFood does not keep one of those cards per vendor. Handing that shared GPU all thirty decoded photos at once blows the device. Micro-batches of eight are how lesson two keeps the vendor folder inside the card. The upload does not set BATCH_SIZE. Lesson eight can override it on submit.

New photos are data in S3. The container image is code and dependencies. Upload more photos, and you sync only. Change describe_items.py or the Dockerfile, and you rebuild, push, and submit again. Mixing those up wastes the afternoon. Either you rebuild an image that did not change, or you skip the push and wonder why the old logic still runs.

The next clip is the upload itself. You will sync a sample folder and list it, without rebuilding the container.
