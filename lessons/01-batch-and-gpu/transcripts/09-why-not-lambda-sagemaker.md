# Video 09 — Why not Lambda or SageMaker here
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What each service optimizes for.**

- **Lambda** — Event-driven, **short** executions, automatic scale per invoke, **no user-chosen GPU attach** in the simple model; package size and `/tmp` limits matter.
- **SageMaker** — **Training jobs**, **real-time endpoints**, feature store, model registry — ML platform with opinionated hosting and autoscaling APIs.
- **Batch** — **Container batch jobs** on EC2 you configure; **start → run → exit**; full control of image and instance type for **minutes-long** GPU work.

**Why not Lambda for this course.** Captioning ~30 photos needs a **large CUDA image**, **GPU memory**, and **multi-minute** runtime. Lambda’s sweet spot is “handle this S3 upload event in 30 seconds,” not “load BLIP and process a folder.”

**Why not SageMaker hosting.** A **real-time endpoint** bills for **always-on** capacity waiting for HTTP requests — great for millisecond fraud scoring, heavy for **twice-a-day vendor folder drops**. SageMaker **batch transform** is closer, but this course teaches **Batch + ECR + bring-your-own-container** — portable skill across render farms, genomics, and ETL.

**Decision slide.** Check **Batch** for offline folder inference; X Lambda (short CPU bursts); X always-on endpoint for this traffic pattern.

Lesson two: the Python **inside** the container — S3 I/O vs GPU — before we Dockerize it.
