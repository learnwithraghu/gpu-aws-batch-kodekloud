# Video 03 — Build context and .dockerignore
**Type:** Theory
**Runtime target:** ~3 minutes

---

Alright. Let's talk about build context.

The build context is every file docker build sends to the Docker daemon from the path you give it. In this course that path is the repo root, the dot at the end of the build command. The daemon doesn't magically see your laptop. It receives a copy of that tree, and the Dockerfile's COPY instructions can only pick files that were inside that copy. A bigger context means a slower build. It also means a higher chance that a secret rides along and gets baked into a layer.

.dockerignore is the filter on that copy. The comment at the top says the context should stay small, and that the image only needs the Dockerfile, the requirements file, and lessons. The patterns drop .git, .github, and .cursor. They drop .env and .env star, and an exception puts .env.example back so the sample file can stay without putting real credentials in the context. They drop docs and helpers, plus PLAN.md, README.md, and syllabus.md. They drop Python cache files and .DS_Store. Credentials for AWS stay in the .aws directory in your home folder, from aws configure. They never belong in an image layer. The job's S3 access is the job role, not a key you copied at build time.

The failure to picture is a Dockerfile that says COPY . . while a real .env is still in the context. Those keys become part of the layer history. Deleting the file in a later commit doesn't erase a layer that already contained it. Our Dockerfile doesn't copy the whole tree. It copies requirements-gpu.txt, then lessons/02-the-container-program/photos.py to /app/photos.py, and describe_items.py to /app/describe_items.py. Even with that care, the ignore file is what keeps .env from being available to a future COPY someone adds in a hurry.

If the context is huge, the first symptom is time. The upload to the daemon drags before pip even starts, and a fifteen to twenty-five minute first build gets blamed on PyTorch when the extra minutes were docs, helpers, and Git history.

lessons isn't in that ignore list, and that's why the COPY of photos.py and describe_items.py can see lessons/02-the-container-program. Ignore the lessons tree by mistake and the build fails on those COPY lines. The filter drops secrets and bulk. It keeps the Dockerfile, requirements-gpu.txt, and the lesson scripts. Docker Desktop has to be running first, or there's no daemon to receive the context at all.

Next you'll set the platform. The g4dn.xlarge is x86_64, and an Apple Silicon laptop won't choose that architecture on its own.
