# Lab 008 — Current manual menu image verification
**Section:** 001 — The Real-World GPU Problem
**Lecture#:** 008
**Sheet title:** [Lab] Current manual menu image verification
**Type:** Lab
**Runtime target:** ~20–30 minutes
**Topic code:** 001-008-[lab]-current-manual-menu-imag

---

## Lab goal

Deploy the Stage 1 KodeFood Vendor Portal on an Amazon Linux EC2 instance, upload menu photos, and submit them for the mocked 24-hour manual review.

## Prerequisites

- AWS account access (console)
- Ability to launch EC2 in a region you can reach (course reference region: `ap-northeast-1`)
- Course repo available on GitHub (or a zip of this repository)

## Steps

### 1. Launch Amazon Linux

1. In the EC2 console, **Launch instance**.
2. Name: `kodefood-vendor-portal`.
3. AMI: **Amazon Linux 2023**.
4. Instance type: `t3.micro` (or free-tier equivalent).
5. Key pair: create or select one for SSH.
6. Network: allow **SSH (22)** and a custom **TCP 8000** inbound rule from *My IP* (preferred) or temporarily `0.0.0.0/0` for a short classroom demo.
7. Launch and note the **public IPv4 address**.

### 2. Clone and start the portal

SSH to the instance, then:

```bash
sudo dnf install -y git   # if git is missing
git clone <YOUR_COURSE_REPO_URL>
cd gpu-aws-batch-kodekloud/lessons/00-the-real-job/vendor_portal
bash setup_ec2.sh
```

Leave the process running in that terminal (or run under `tmux`/`screen`).

### 3. Use the vendor UI

1. Open `http://<public-ip>:8000`.
2. Upload at least three images (include one non-food photo if you have one).
3. Confirm each card shows **Pending Manual Review**.
4. Click **Submit Menu Photos**.
5. Confirm the banner:
   > One of your account managers will review this in 24 hours and get back to you.

### 4. Optional local mode

If EC2 is unavailable, you may complete the same UI flow on your laptop:

```bash
cd lessons/00-the-real-job/vendor_portal
bash run_portal.sh
# http://127.0.0.1:8000
```

Still document that the intended teaching path is Amazon Linux on EC2.

## Deliverable

Paste or screenshot:

1. The portal URL (or localhost).
2. The submitted gallery with pending badges.
3. The 24-hour account-manager banner.

One short sentence: why this process does not scale when vendor volume grows.

## Cleanup

Stop or terminate the EC2 instance when finished so it does not idle overnight. Stage 2 (Section 007) can reuse a new small instance later if needed.

## Common issues

| Symptom | Fix |
|---------|-----|
| Browser cannot connect | Check security group TCP 8000; confirm `setup_ec2.sh` is still running |
| `Permission denied` on scripts | `chmod +x setup_ec2.sh run_portal.sh` |
| Upload does nothing | Use jpg/png; check the flash message for invalid types |
