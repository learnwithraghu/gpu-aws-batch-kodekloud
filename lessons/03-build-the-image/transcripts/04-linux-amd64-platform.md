# Video 04 — Build for linux/amd64
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What `--platform linux/amd64` does.** Produces an **x86_64** image even on **ARM** Macs. **`g4dn`** is x86_64.

**Why it matters.** **arm64** images **push to ECR fine** then **fail at run** on Batch — confusing because push succeeded.

**Analogy.** EU vs US plug — same appliance design, wrong physical connector.

**Visual:** M1 laptop → amd64 image → green on g4dn; arm64 → red X at run.

Layer caching — next.
