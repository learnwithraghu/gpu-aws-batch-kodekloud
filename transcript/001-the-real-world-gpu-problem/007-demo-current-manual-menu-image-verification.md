# Demo 007 — Current manual menu image verification
**Section:** 001 — The Real-World GPU Problem
**Lecture#:** 007
**Sheet title:** [Demo] Current manual menu image verification
**Type:** Demo
**Runtime target:** ~8–10 minutes
**Topic code:** 001-007-[demo]-current-manual-menu-ima

---

## Teaching goal

Show the **legacy** KodeFood vendor experience before any GPU or AWS Batch work. Vendors upload menu photos through a simple portal. The system does not caption or accept/reject them. It only queues a human review with a 24-hour promise.

That bottleneck is the problem the rest of the course solves.

## Before you record

1. Launch (or reuse) an Amazon Linux 2023 `t3.micro` with inbound **SSH 22** and **TCP 8000** from your IP.
2. Clone the course repo on the instance and start Stage 1:

```bash
cd gpu-aws-batch-kodekloud/lessons/00-the-real-job/vendor_portal
bash setup_ec2.sh
# MODE defaults to manual
```

3. Open `http://<public-ip>:8000` in a browser. Keep a few dish photos (and optionally a selfie or logo) ready to upload.
4. Optional local dry run: `cd lessons/00-the-real-job/vendor_portal && bash run_portal.sh`

Lesson notes: [`lessons/00-the-real-job/README.md`](../../lessons/00-the-real-job/README.md). Portal setup: [`vendor_portal/README.md`](../../lessons/00-the-real-job/vendor_portal/README.md).

## Demo script (spoken flow)

1. **Frame the product.** KodeFood needs trustworthy menu photos. Today the “backend” for vendors is this portal on a plain EC2 box — no GPU, no Batch.
2. **Show the upload UI.** Select several images in menu order. Click **Add to gallery**. Point at the **Pending Manual Review** badges.
3. **Submit.** Click **Submit Menu Photos**. Read the banner aloud:
   > Submitted! One of your account managers will review this in 24 hours and get back to you.
4. **Name the pain.** At a few vendors this is fine. At hundreds of vendors per week, the human queue is the product. Bad photos can still reach the menu; good photos wait unpublished.
5. **Tease the destination.** Later we will keep the same 24-hour *cadence* for vendors, but replace the account manager with a **nightly AWS Batch GPU job** that writes captions and accept/reject decisions into a CSV. Section 007 brings that CSV back into this portal.

## What not to do in this demo

- Do not create S3 buckets, ECR, or Batch resources yet.
- Do not switch `MODE=batch` here — that is Section 007 Demo 005.
- Do not imply real-time inference is the goal; the SLA stays asynchronous.

## Checkpoint for students

After this demo, students should be able to say: *uploads go into a pending human queue with a 24-hour review message; scale turns that into a systems problem, not a staffing problem.*
