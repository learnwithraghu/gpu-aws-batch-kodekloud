# Video 06 — Demo: ECR login and push
**Type:** Demo  
**Runtime target:** ~3–4 minutes

---

**Purpose.** Publish local **`gpu-teaching:latest`** where Batch can pull it.

**`.env`** for registry host / **`ECR_IMAGE_URI`**. **`get-login-password`** → **`docker login`**. Tag image with full URI. **`docker push`**. Verify **`describe-images`** or console — new **`latest`** timestamp.

**Segue:** lesson five — S3 buckets for photos and CSV.
