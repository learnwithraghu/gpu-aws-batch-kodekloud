# Video 01 — Why containers for GPU jobs
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What a container is.** A **filesystem + runtime config** packaged with your app, started as an isolated process on a host. For ML, it pins **CUDA user-space libraries**, **PyTorch**, **Python deps**, and **your scripts** into one pullable artifact.

**Why Batch uses containers.** Every run must see the **same stack** — no “works on my laptop” because the cluster pip-installed a different **`transformers`**. Containers are how CI/CD at Shopify-style companies ship **reproducible** inference workers.

**Host vs image split.** **AMI** provides **drivers + ECS**; **image** provides **CUDA runtime + app**. Missing either breaks GPU jobs.

**In this course.** Dockerfile copies lesson two files to **`/app`**; Batch never sees your repo tree directly.

**Visual:** Host layer + container layer stack; both required for CUDA true.

Base image and pinning — next.
