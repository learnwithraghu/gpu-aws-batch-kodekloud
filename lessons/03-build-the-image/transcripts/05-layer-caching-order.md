# Video 05 — Layer caching
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

Docker builds an image as a stack of layers, and it reuses a layer when the instruction and the inputs it depends on haven't changed. That reuse is the cache. The order of the instructions decides which edits are cheap and which edits throw away the slow work. In this Dockerfile the order is the base image, then the requirements install, then the application code.

Read it from the top. FROM pulls pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime. WORKDIR sets /app. COPY brings in requirements-gpu.txt. RUN pip install --no-cache-dir -r requirements-gpu.txt installs transformers at four point forty-six point three, plus Pillow, boto3, and python-dotenv. Only after that do the two COPY lines run. photos.py goes to /app/photos.py. describe_items.py goes to /app/describe_items.py. The heavy step is the pip layer, sitting under the thin copy of the two scripts. That's deliberate. Your code changes more often than the pin.

Change describe_items.py, or change photos.py, and Docker can reuse the base and the pip layer. It rebuilds the thin COPY layers on top. That's a fast rebuild, on the order of minutes, because you're not downloading the CUDA base again and you're not reinstalling the Python packages. Change requirements-gpu.txt and the pip instruction is no longer a cache hit. Pip runs again, and you're back in the slow path. Change the Dockerfile itself, in a way that invalidates those lines, and the same thing happens. The cache key is the instruction plus the files it copies. A comment-only story in your head doesn't keep a layer if the inputs moved.

The first build has no cache to reuse. It downloads the CUDA base and installs the pip packages. Plan on fifteen to twenty-five minutes. A later build reuses the cache unless you changed the Dockerfile, requirements-gpu.txt, photos.py, or describe_items.py. When you're iterating on a prompt or on the CSV path, you want that second shape. You edit the Python, you build again, and the pip layer comes back labeled as already done.

If the Python files were copied before the pip install, every one-line edit to describe_items.py would reinstall transformers. The T4-sized logic in the script would be cheap to change and expensive to ship. The file is ordered so the rare change, the pin, sits below the common change, the two scripts.

Say the edit is the prompt, the string a photography of, or num_beams, inside describe_items.py. requirements-gpu.txt didn't change, and the Dockerfile didn't change. Docker rebuilds from the COPY of that script downward and reuses the base and the pip layer. You wait minutes, not another fifteen to twenty-five. The local image is new. The registry isn't, until you push. The cache shortens the rebuild on your laptop. It doesn't update the image Batch pulls.

On the screen, stack four layers and mark the bottom ones cached when only describe_items.py has changed. Base, then pip, then photos.py if it didn't change, and a fresh top layer for describe_items.py. When you save requirements-gpu.txt, wipe the cached mark off the pip layer and everything above it.

A fast rebuild still lives on your laptop. Next you'll separate the local tag gpu-teaching:latest from the image Batch will actually pull.
