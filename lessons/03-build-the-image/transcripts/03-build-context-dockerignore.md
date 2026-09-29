# Video 03 — Build context and .dockerignore
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What build context is.** All files sent to **`docker build`** from the path you specify (repo root). Bigger context = slower builds + risk of copying **secrets**.

**Why `.dockerignore` exists.** Exclude **`.env`**, **`.git`**, large unrelated folders — credentials stay in **`~/.aws/`**, not image layers.

**Example failure.** Accidentally **`COPY . .`** with `.env` in context → keys baked into history — security incident.

**Visual:** Filter funnel shrinking context size.

`linux/amd64` — next.
