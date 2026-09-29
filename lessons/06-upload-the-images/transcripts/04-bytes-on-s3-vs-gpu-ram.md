# Video 04 — Bytes on S3 versus GPU memory
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

A few megabytes in S3 is the size of the file at rest. It is not the size of the work the GPU does. The job downloads the jpeg, which is small and compressed. photos.py opens those bytes and converts them to an RGB picture. That decoded picture is much larger than the file you uploaded. describe_items.py then turns a group of those pictures into tensors on the device and runs the caption model. The batch on the GPU is larger still. Peak memory follows the decoded group, not the sum of jpeg sizes in the bucket.

That is why BATCH_SIZE counts photos. The default is eight. Thirty photos become four passes, eight, then eight, then eight, then six. Each pass is one GPU forward. The sentences append to one list. At the end, one CSV is written. The groups are a memory tactic. They are not extra output files. You do not choose the group size by adding up megabytes on S3 and cutting the folder when the total crosses a line. Eight small photos and eight huge photos are both a batch of eight, and they do not cost the same device memory.

The course example is resolution. Eight photos at twelve megapixels in one pass can run out of GPU memory where eight photos at two megapixels succeed. Same count, same model, different decoded size. If that happens, the knobs later are a smaller BATCH_SIZE, or a resize before the tensor is built. This lesson does not do that resize. It only tells you why the count exists. Large files have a second cost before the GPU starts. They take longer to download, and the CPU spends longer decoding them into RGB. A job can look stuck in the download and still be healthy.

The instance underneath is a g4dn.xlarge, one T4, and the model is loaded once for the whole folder. Handing that GPU all thirty decoded photos at once is how a small catalog blows the device. Micro-batches of eight are how lesson two keeps the same folder inside the card. The upload does not set BATCH_SIZE. Lesson eight can override it on submit. The photos you sync here are the input to that count.

New photos are data. They live in S3. The container image is code and dependencies, describe_items.py, the model libraries, the CUDA stack baked in lessons three and four. Upload more photos, and you sync only. You do not rebuild. Change describe_items.py or the Dockerfile, and you rebuild, push, and submit again. Mixing those up wastes the afternoon in one of two ways. You rebuild an image that did not change, and you wait on a push the GPU never needed. Or you change the caption code, skip the push, submit the old image, and wonder why the new logic never runs. The job runs whatever was baked into the tag it pulled.

On the screen, a small jpeg icon sits on the left, labeled with a few megabytes. It expands into a wide RGB block, then into a taller block on the GPU labeled as a batch of eight. The S3 number never matches the GPU number. The arrow between them is decode, not upload.

The next clip is the upload itself. You will sync a sample folder and list it, and you will not rebuild the container to do that.
