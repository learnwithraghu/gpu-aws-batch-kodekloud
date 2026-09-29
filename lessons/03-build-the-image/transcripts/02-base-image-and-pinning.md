# Video 02 — Base image and dependency pinning
**Type:** Theory
**Runtime target:** ~3 minutes

---

Okay, so the base image is the parent filesystem, the line FROM in the Dockerfile.

This course starts from pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime, PyTorch two point one point zero, CUDA eleven point eight, cuDNN eight, runtime. That image already ships Linux, the CUDA eleven point eight runtime libraries, and a PyTorch build compiled against that CUDA. The hard compatibility triangle is solved by the PyTorch maintainers before you write a line. You add only requirements-gpu.txt and the two lesson two files.

Building CUDA, cuDNN, and PyTorch from scratch inside every Dockerfile is possible, and it's weeks of engineering. For teaching batch inference you want the short version. Start from a maintained PyTorch plus CUDA image, then install your requirements and copy your scripts.

What this Dockerfile adds is small, and the versions are the point. It runs pip install with --no-cache-dir, from requirements-gpu.txt. That file pins transformers to version four point forty-six point three, written as transformers==4.46.3. It also installs Pillow, boto3, and python-dotenv. Newer transformers releases require PyTorch two point five or newer and break BLIP on Batch. On this two point one base, an unpinned pip install transformers can resolve to a release that fails at import or disables itself. The GPU job then exits before it describes a photo. You get no CSV.

Pinning is how you keep last week's working image from breaking when a fresh install resolves to a different major line.

Here's the failure if you delete the pin. The rebuild succeeds. The push succeeds. Batch marks the job FAILED in about thirty seconds. The container exits with code one. CloudWatch shows an ImportError. That's not a Batch scheduling bug. The image booted and the import of transformers died. Put the pin back, rebuild, and push again.

Follow that failure into the program. load_model reaches BlipProcessor.from_pretrained and BlipForConditionalGeneration.from_pretrained for Salesforce/blip-image-captioning-base. If transformers can't import on this PyTorch, main never gets to photos.list_photo_keys, and save_csv never runs. The vendor folder stays unread. The pin at four point forty-six point three is what keeps that import on a path the two point one image can run. Pillow and boto3 ride along because the scripts decode images and call S3. python-dotenv is in that file too. The scripts themselves still read the job environment with os.environ.

Next you'll see what the build context is, and why .dockerignore keeps secrets out of those layers.
