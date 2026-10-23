# Demo 005 — Final End-to-End Pipeline Walkthrough
**Section:** 008 — Production GPU Pipeline Design
**Lecture#:** 005
**Sheet title:** [Demo] Final End-to-End Pipeline Walkthrough
**Type:** Demo
**Runtime target:** ~10–12 minutes
**Topic code:** 008-005-[demo]-final-end-to-end-pipeli

---

## Teaching goal

Close the loop from Section 001. The same KodeFood Vendor Portal now shows **automated** nightly decisions: captions and accept/reject marks from `descriptions.csv`, produced by the AWS Batch GPU job — not by an account manager.

Vendors still wait on the order of hours (a nightly job), but the bottleneck is compute scheduling, not human review.

## Before you record

You need a catalog CSV in the Batch contract shape:

```csv
image_s3_uri,item_description,photo_status
```

**Path A — live Batch output (preferred if a job already succeeded):**

```bash
# From a machine with AWS CLI creds / or the EC2 instance role
export MODE=batch
export S3_CSV_BUCKET=gpu-teaching-captions-csv-<account-id>
export IMAGE_STEM=sample   # matches descriptions/sample/descriptions.csv
cd gpu-aws-batch-kodekloud/lessons/00-the-real-job/vendor_portal
bash run_portal.sh   # or setup_ec2.sh on Amazon Linux
```

Confirm the object exists:

```bash
aws s3 cp "s3://${S3_CSV_BUCKET}/descriptions/${IMAGE_STEM}/descriptions.csv" -
```

**Path B — sample CSV (always works for recording):**

```bash
cd gpu-aws-batch-kodekloud/lessons/00-the-real-job/vendor_portal
MODE=batch bash run_portal.sh
# loads sample_data/descriptions.csv
```

Optional: briefly reopen Stage 1 (`MODE=manual`) in another tab or a prior clip so the contrast is visual.

Live queue / job definition names: [`docs/aws-batch-setup.md`](../../docs/aws-batch-setup.md). Portal env vars: [`vendor_portal/README.md`](../../lessons/00-the-real-job/vendor_portal/README.md).

## Demo script (spoken flow)

1. **Recall Stage 1.** In Section 001 the portal said an account manager would review uploads in 24 hours. That was a human queue.
2. **Name what changed underneath.** Photos land under `images/<stem>/`. A GPU Batch job runs `describe_items.py`, writes `descriptions/<stem>/descriptions.csv`, and scales the fleet toward zero when the queue is empty. A nightly schedule fits the same vendor SLA without keeping reviewers online.
3. **Open Stage 2.** Show `MODE=batch`. Read the green banner:
   > Nightly GPU Review Complete — Processed automatically via AWS Batch
4. **Walk the counters.** Total / Accepted / Rejected. Point at food rows vs selfie / car / logo rejects.
5. **Show the catalog table.** Columns match the product contract: `image_s3_uri`, `item_description`, `photo_status`. The customer-facing menu reads this file; it does not call the model on every request.
6. **Production takeaway.** Asynchronous SLA + durable S3 contract + ephemeral GPU workers. Batch is the right shape when work arrives in folders, latency of hours is acceptable, and you refuse to pay for idle GPUs.

## Optional one-minute architecture flashback

```
Vendor UI / uploads → S3 images/<stem>/
                   → AWS Batch GPU job
                   → S3 descriptions/<stem>/descriptions.csv
                   → Vendor UI (MODE=batch) renders accepted/rejected
```

## What not to do in this demo

- Do not rebuild ECR or re-register the job definition unless something is broken.
- Do not claim results are real-time; keep the “nightly / within 24 hours” framing.
- Do not hide rejected rows — operations needs them in the CSV.

## Checkpoint for students

Students should be able to contrast: *Stage 1 = human review in 24 hours; Stage 2 = same cadence, GPU Batch decisions in the portal via `descriptions.csv`.*
