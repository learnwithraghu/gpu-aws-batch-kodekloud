# Video 01 — What Batch actually runs
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

AWS Batch starts one command inside a container image. For this course that command is python /app/describe_items.py. The path /app/describe_items.py is a location on the image filesystem, the files inside the container, not a path in your Git checkout. The Dockerfile instruction COPY is what places describe_items.py at that path. The command that starts it's either the default stored on the job definition or an override you pass when you submit. Both of those start bytes that were already baked into the image.

describe_items.py is the file Batch starts, and that file imports photos.py. Lesson three copies both of them into the image, at /app/photos.py and /app/describe_items.py. The copy on your laptop is only the source. You edit it, you save, and Git shows a diff. Batch never reads that disk. It pulls immutable image layers from ECR and runs whatever was baked in at /app/. After lesson four, that registry copy is the program. Until you rebuild and push, a job keeps running the old bytes. People on an app store keep opening last week's build while the engineers edit the next one on their laptops. Your editor and the registry are two different clocks.

Walk the same folder, images/sample, down two timelines. On the first timeline you change the caption prompt in describe_items.py, you save, and you submit. The CSV comes back with the same sentences as the previous run. ECR still holds the previous image, so the captions stay put. Saving the file never reached the machine that runs the job. On the second timeline you make that same edit, then you run docker build, then docker push, then you submit. The new sentences show up, because the digest Batch pulls has changed. The push is the step that updates production.

This lesson stops at the source. You read the two Python files. You don't submit a job. A vendor folder is already in S3. The program reads that folder and writes one CSV. It doesn't create the buckets, the registry, or the Batch environment. Those belong to other lessons. Packaging the image is lessons three and four. Scheduling that image on a GPU machine is lessons seven and eight. A change to either Python file stays invisible to Batch until the image is built and pushed again.

A commit in Git records the source. It doesn't publish a new image. docker build writes the layers on your laptop. docker push is what stores them in ECR. Batch pulls that stored image when the job starts. Skip the push, and an override still starts python /app/describe_items.py, which is the old file COPY baked in last time. The captions stay on the previous behavior because the digest never moved.

On the screen, put the laptop on the left with describe_items.py open in Git, and ECR on the right with one image digest. The submit arrow leaves the registry. The only arrow that replaces that digest is the push.

That one command is still a single process, and the work inside it's split across two files. Next you'll see why the S3 work and the GPU work don't live in the same file, and how a failure in one of them looks different from a failure in the other.
