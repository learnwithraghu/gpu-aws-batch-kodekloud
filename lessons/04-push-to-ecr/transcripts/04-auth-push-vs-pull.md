# Video 04 — Push auth vs pull auth
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**Push (developer).** **`aws ecr get-login-password`** → **`docker login`** — **~12 hour** token. IAM user/role needs **push** permissions.

**Pull (EC2).** **Instance profile** **`ecsInstanceRole`** — no laptop keys on GPU box.

**Why never bake AWS keys in images.** Layers leak in history; roles rotate cleanly.

**Visual:** Human → temporary login; EC2 → instance role → pull.

Layer upload + scan — next.
