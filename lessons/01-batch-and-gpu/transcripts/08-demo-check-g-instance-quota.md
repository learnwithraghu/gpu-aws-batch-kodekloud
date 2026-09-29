# Video 08 — Demo: check G/VT on-demand quota
**Type:** Demo  
**Runtime target:** ~3–4 minutes

---

**Why this demo exists.** **`RUNNABLE`** jobs generate panic edits to Dockerfiles. One CLI call answers: “Is my account **allowed** to launch on-demand **`g4dn`** at all?” That is **quota**, not application code.

Terminal, region **`ap-northeast-1`**. Run **`aws service-quotas get-service-quota`** with **`service-code ec2`**, **`quota-code L-DB2E81BA`**, query **`QuotaName`** and **`Value`**.

**If Value is 0**, narrate the full stuck-job story: healthy on-demand CE, empty CloudWatch, jobs never start. Show console path: Service Quotas → EC2 → **Running On-Demand G and VT instances** → request **8** vCPUs for headroom. Mention approval delay — stay on **Spot queue** meanwhile.

**If Value ≥ 4**, clarify: on-demand is **permitted**, not **guaranteed**; Spot may still be the right default for cost.

Point at **`helpers/watch_batch_job.sh`** — lesson eight uses it during wait.

**Visual on screen:** quota value large font; arrow to “on-demand fallback OK / blocked”.

Why Lambda and SageMaker are not our primary tools — final clip this lesson.
