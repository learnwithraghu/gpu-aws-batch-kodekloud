# Video 01 — What Batch actually runs
**Type:** Theory
**Runtime target:** ~3 minutes

---

Alright. Welcome back. In this lesson we look at the program Batch actually runs.

AWS Batch starts one command inside a container image. For this course that command is python /app/describe_items.py. The path /app/describe_items.py is a location on the image filesystem, not a path in your Git checkout. The Dockerfile instruction COPY is what places describe_items.py at that path. The command that starts it is either the default stored on the job definition or an override you pass when you submit. Both start bytes that were already baked into the image.

describe_items.py is the file Batch starts, and that file imports photos.py. Lesson three copies both into the image, at /app/photos.py and /app/describe_items.py. The copy on your laptop is only the source. You edit it, you save, and Git shows a diff. Batch never reads that disk. It pulls immutable image layers from ECR and runs whatever was baked in at /app/. After lesson four, that registry copy is the program. Until you rebuild and push, a job keeps running the old bytes. Your editor and the registry are two different clocks.

Walk the same folder, images/sample, down two timelines. On the first you change the caption prompt in describe_items.py, you save, and you submit. The CSV comes back with the same sentences. ECR still holds the previous image. On the second you make that same edit, then you run docker build, then docker push, then you submit. The new sentences show up, because the digest Batch pulls has changed. The push is the step that updates production.

This lesson stops at the source. You read the two Python files. You don't submit a job. A vendor folder is already in S3. The program reads that folder and writes one CSV with accepted and rejected rows. It doesn't create the buckets, the registry, or the Batch environment. Packaging the image is lessons three and four. Scheduling that image on a GPU is lessons seven and eight. A change to either Python file stays invisible to Batch until the image is built and pushed again.

A commit in Git records the source. It doesn't publish a new image. docker build writes the layers on your laptop. docker push stores them in ECR. Skip the push, and an override still starts the old file COPY baked in last time.

That one command is still a single process split across two files. Next you'll see why the S3 work and the GPU work don't live in the same file.
