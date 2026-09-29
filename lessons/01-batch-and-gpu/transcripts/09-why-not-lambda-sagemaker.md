# Video 09 — Why not Lambda or SageMaker here
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

Lambda, SageMaker, and Batch are each built for a different shape of work. Knowing the shape is how you pick.

Lambda is event driven. Each run is short, and it scales on its own per invoke. In the simple model you do not choose a GPU and attach it. Package size matters, and so does the temporary disk at /tmp. The sweet spot is, handle this S3 upload event in about thirty seconds.

SageMaker is an ML platform. Training jobs, real-time endpoints, a feature store, a model registry, plus hosting and autoscaling APIs that already have an opinion. A real-time endpoint bills for capacity that stays up waiting for HTTP. That is a strong fit for millisecond fraud scoring. It is a heavy fit for a vendor folder that shows up twice a day.

Batch runs a container job on EC2 you configure. The job starts, it runs, and it exits. You control the image and the instance type, which is what you want for minutes of GPU work. Captioning about thirty photos needs a large CUDA image, GPU memory enough to load BLIP, and a runtime of more than a few seconds. That folder is the job Batch is for. Lambda's thirty-second event handler is a different job.

SageMaker batch transform is closer than a hosted endpoint, because it is also offline work on a pile of inputs. This course still teaches Batch, plus ECR, plus a container you bring yourself. You already know the shape. Photos in S3, an image in ECR with CUDA and the model, one GPU, a run that ends when the CSV exists. Batch is the smaller piece of machinery for a rare, folder-sized batch of photos. A hosted endpoint would bill you to wait for the next vendor. A Lambda invoke would have to finish inside a short timeout, with limited disk, and without a simple way to attach one T4 for a few minutes at this image size and this model download.

That combination is a portable skill. The same pattern shows up in render farms, in genomics, and in ordinary ETL. You queue a container, a GPU starts, the work finishes, the GPU stops. The decision for this traffic is offline folder inference on Batch. Short CPU bursts can stay on Lambda. An always-on endpoint can stay where the calls never pause. This catalog pauses for hours.

On the screen, a decision slide has three rows. Offline folder inference is checked under Batch. Lambda is crossed out, because this is not a short CPU burst. An always-on endpoint is crossed out, because this traffic is a rare drop, not a stream of HTTP calls waiting on a hot GPU.

Lesson two is the Python inside that container. It starts with the command Batch actually runs, and with why the image in ECR is the program that executes, before that program is put in a Dockerfile.
