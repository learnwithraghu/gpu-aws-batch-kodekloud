# Video 03 — Region and location constraint
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What region choice affects.** Latency, data residency, **same-region** access with Batch/ECR, billing.

**Why `LocationConstraint` outside us-east-1.** API requires explicit region on **`create-bucket`** in Tokyo (**`ap-northeast-1`**) — us-east-1 is default legacy exception.

**Example mistake.** Buckets in **us-west-2**, Batch in **Tokyo** — cross-region egress, slower jobs, confused students.

**Visual:** Single region pin with Batch + ECR + both buckets stacked.

Two buckets — next.
