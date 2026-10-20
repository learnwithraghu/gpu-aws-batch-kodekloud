# KodeFood Vendor Portal

Part of [Lesson 00 — The real job](../README.md). Used in:

| Stage | `MODE` | Course slot | What students see |
|-------|--------|-------------|-------------------|
| 1 — Manual review | `manual` (default) | Section 001 Demo 007 / Lab 008 | Upload dish photos → *"One of your account managers will review this in 24 hours…"* |
| 2 — Nightly GPU Batch | `batch` | Section 007 Demo 005 | Catalog from `descriptions.csv` with **accepted** / **rejected** marks |

No GPU is required for either stage of the portal. Stage 2 only *displays* the CSV that the Batch GPU job already wrote.

## Quick start (local)

```bash
cd lessons/00-the-real-job/vendor_portal
bash run_portal.sh
# open http://127.0.0.1:8000
```

Stage 2 with the bundled sample CSV:

```bash
cd lessons/00-the-real-job/vendor_portal
MODE=batch bash run_portal.sh
```

Stage 2 from a real Batch output:

```bash
export MODE=batch
export S3_CSV_BUCKET=gpu-teaching-captions-csv-<account-id>
export IMAGE_STEM=sample   # -> descriptions/sample/descriptions.csv
bash run_portal.sh
```

Or point at a local file:

```bash
MODE=batch DESCRIPTIONS_CSV=./sample_data/descriptions.csv bash run_portal.sh
```

## EC2 demo (Amazon Linux)

1. Launch an **Amazon Linux 2023** `t3.micro` (or similar) from the AWS console.
2. Security group: allow inbound **TCP 8000** from your IP (and **SSH 22** if you use SSH).
3. Clone this repo onto the instance, then:

```bash
cd gpu-aws-batch-kodekloud/lessons/00-the-real-job/vendor_portal
bash setup_ec2.sh
```

4. Browse to `http://<public-ip>:8000`.

For Stage 2 on the same instance after a Batch job has written the CSV:

```bash
export MODE=batch
export S3_CSV_BUCKET=gpu-teaching-captions-csv-<account-id>
export IMAGE_STEM=sample
# Instance role (or AWS CLI creds) needs s3:GetObject on the CSV bucket
bash setup_ec2.sh
```

## Environment variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `MODE` | `manual` | `manual` or `batch` |
| `PORT` | `8000` | HTTP listen port |
| `S3_CSV_BUCKET` | empty | Load `descriptions/<IMAGE_STEM>/descriptions.csv` from S3 |
| `IMAGE_STEM` | `sample` | Stem folder under `descriptions/` |
| `DESCRIPTIONS_CSV` | empty | Local CSV path (wins over S3 when set) |

CSV columns match the Batch contract: `image_s3_uri`, `item_description`, `photo_status`.

## Layout

```
vendor_portal/
  app.py                 # Flask app
  run_portal.sh          # local / EC2 start helper
  setup_ec2.sh           # Amazon Linux bootstrap + start
  requirements.txt
  templates/             # manual.html, batch.html
  static/style.css
  sample_data/descriptions.csv
  uploads/               # Stage 1 local uploads (gitignored contents)
```
