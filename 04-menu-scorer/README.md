# 04 — ML menu satisfaction scorer

A minimal ML scoring script ([score_menu.py](score_menu.py)) that evaluates dish photos on a **1.0–10.0** menu satisfaction scale using three visual quality features: **brightness**, **contrast**, and **sharpness**.

In module **05**, this same scoring code runs inside **AWS Batch** against photos uploaded to S3 in step 03. In this module, we build and test the scorer locally first.

## Decision rule

- **Score `>= 8.0` (`APPROVED`)**: High menu satisfaction — dish photo can be used in the KodeFood app.
- **Score `< 8.0` (`REJECTED`)**: Low menu satisfaction — dish photo cannot be used in the app and needs a brighter, clearer photo.

## Test locally with `uv`

From the repo root (uses the sample photos in [`images/`](../images/)):

```bash
uv run 04-menu-scorer/score_menu.py
```

Or create a virtual environment in `04-menu-scorer/` with `uv`:

```bash
cd 04-menu-scorer
uv venv
uv pip install -r requirements.txt
uv run score_menu.py
```

You can also pass a custom local folder:

```bash
uv run 04-menu-scorer/score_menu.py path/to/photos
```

## Optional: preview against your S3 bucket from Step 03

Before moving this into AWS Batch in module 05, you can also point the scorer at `s3://kodefood-menu-uploads-kodekloud/uploads/`:

```bash
uv run 04-menu-scorer/score_menu.py --s3
```

Override the bucket or prefix with `S3_BUCKET` and `S3_PREFIX` if needed:

```bash
S3_BUCKET=your-bucket-name uv run 04-menu-scorer/score_menu.py --s3
```
