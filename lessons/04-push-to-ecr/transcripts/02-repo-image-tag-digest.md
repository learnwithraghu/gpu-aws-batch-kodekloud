# Video 02 — Repository, image, tag, digest
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**Repository — what it is.** A **named collection** of images in ECR, like a GitHub repo name **`gpu-teaching`**. It holds many pushes over time.

**Image — what it is.** The **actual content**: ordered **layers** (filesystem diffs) plus metadata. Identified uniquely by **digest** (`sha256:…`) — content-addressed, **immutable**.

**Tag — what it is.** A **human-readable pointer** (`latest`, `v1`, `git-abc123`) to **one digest at a time**. Tags are **mutable** unless you use policies; digests are not.

**Why three words get conflated.** People say “push the image to ECR” meaning “upload layer stack and move a tag.” Incident calls need precision: “Which **digest** ran on job **`abc`**?” not “we use latest.”

**Example push story.** Monday push → digest **A**, **`latest` → A**. Tuesday push → digest **B**, **`latest` → B**. Job definition still says **`…/gpu-teaching:latest`** — Wednesday’s job runs **B** without editing the definition. Monday’s **A** still exists if you reference digest directly.

**Batch connection.** Job definition **`image`** field is a string URI — usually tag form. Scheduler resolves tag to digest at pull time on the instance.

**Visual:** Repo box; digests A/B as boxes; tag **`latest`** arrow moving from A to B on second push.

Mutable **`latest`** teaching tradeoff — next.
