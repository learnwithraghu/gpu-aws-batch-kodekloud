# Video 07 — Demo: docker build
**Type:** Demo
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

I'm building the image on this machine, with the architecture Batch's g4dn.xlarge can run, and I'm stopping before any push. Docker Desktop is running. I'm at the repo root, because the COPY paths start with lessons/02-the-container-program. If I build from the wrong directory, those paths don't resolve.

I open the Dockerfile and read it in order. FROM is pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime. That's PyTorch two point one point zero, CUDA eleven point eight, cuDNN eight, runtime. WORKDIR /app makes /app the working directory, which is also where the scripts will import each other. COPY requirements-gpu.txt . brings the pin file in. RUN pip install --no-cache-dir -r requirements-gpu.txt installs it. I want you to notice transformers==4.46.3 in that file, version four point forty-six point three, plus Pillow, boto3, and python-dotenv. A newer transformers release requires PyTorch two point five or newer and breaks BLIP on this base. The pin is what this RUN line actually installs.

The next two lines are the program, and they come after pip so a code edit can reuse this layer. COPY lessons/02-the-container-program/photos.py to /app/photos.py. COPY lessons/02-the-container-program/describe_items.py to /app/describe_items.py. Both files land in /app, so describe_items.py can import photos. The command Batch will use later is python /app/describe_items.py. There's no GPU pass in this clip. I'm only baking the files in.

In the terminal I run docker build --platform linux/amd64 -t gpu-teaching:latest . The platform flag forces linux/amd64, an x86_64 image, even on an Apple Silicon Mac that would otherwise build arm64. The -t flag names the local tag gpu-teaching:latest. The dot is the build context, the repo root. .dockerignore is what keeps .env, .git, docs, and helpers out of that context. The first build downloads the CUDA base and runs the pip install. I plan on fifteen to twenty-five minutes. A later build, when I have only changed photos.py or describe_items.py, reuses the cached pip layer and finishes much faster. If I had changed requirements-gpu.txt, pip would run again.

While it runs, I watch the order match the file. On a cold build the base download is most of the fifteen to twenty-five minutes. The pip install is next, and that's where transformers stays on four point forty-six point three. The two COPY lines are last, and they're quick. If Docker reports a layer cached, I want that on the base and on pip, and only when I've changed a script since the last build. I don't swap the tag. gpu-teaching:latest is the name lesson four pushes, and it's the name I'll ask docker images to show. I also don't drop --platform linux/amd64 to make an Apple Silicon build feel faster. Faster and wrong is an arm64 image wearing this same tag. The g4dn can't run it, and that failure waits until job time, after a push that looked clean.

When the build exits, I run docker images gpu-teaching. I want the local tag gpu-teaching:latest, and a size of several gigabytes. That tag is on this laptop. Batch can't pull it from here.

Lesson four is the registry. Batch only starts a container it can pull from ECR, and the next clip is why that registry has to exist before a worker can run this image.
