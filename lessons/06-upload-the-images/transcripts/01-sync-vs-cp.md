# Video 01 — sync vs cp
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What `aws s3 cp` does.** Copy **file or tree** — one-shot or recursive — good for single objects.

**What `aws s3 sync` does.** **Mirror** local directory to prefix — upload **new/changed**, skip matches — ideal for **25–30 photo vendor drops** and incremental adds.

**Example.** Vendor sends 3 retakes — sync uploads **3**, not 30.

**Visual:** Sync compares checksums; only delta uploads highlighted.

Prefix contract — next.
