# Video 01 — What Batch actually runs
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What it is.** The **container entry process** for this course is **`python /app/describe_items.py`** — a file path **inside the image filesystem**, set by Dockerfile **`COPY`** and by **command** (default or override).

**Why laptop code ≠ cloud behavior.** Developers edit Git on disk; Batch executes **immutable image layers** from ECR. Until **rebuild + push**, production runs **old bytes** — like users on the App Store running last week’s build while engineers edit locally.

**Example two timelines.** **A:** edit Python → save → submit → **same captions** (stale image). **B:** edit → **`docker build`** → **`docker push`** → submit → **new behavior**.

**In this lesson.** Read and understand source; no submit yet. Packaging is lessons three–four; scheduling is seven–eight.

**Visual:** Laptop Git vs ECR digest; only push updates what Batch pulls.

Splitting S3 code from GPU code — next.
