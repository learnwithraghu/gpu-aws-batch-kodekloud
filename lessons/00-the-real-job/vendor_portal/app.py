"""KodeFood Vendor Portal — Stage 1 manual review and Stage 2 Batch decisions.

Modes (env MODE):
  manual  — Section 001: upload locally, "account manager will review in 24 hours"
  batch   — Section 007: show nightly GPU Batch CSV (accepted / rejected)

Optional Batch mode env:
  S3_CSV_BUCKET   — bucket with descriptions/<stem>/descriptions.csv
  IMAGE_STEM      — folder stem (default: sample)
  DESCRIPTIONS_CSV — local CSV path (overrides S3 when set)
"""
from __future__ import annotations

import csv
import io
import os
import uuid
from pathlib import Path

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
SAMPLE_CSV = BASE_DIR / "sample_data" / "descriptions.csv"

MODE = os.environ.get("MODE", "manual").strip().lower()
if MODE not in ("manual", "batch"):
    MODE = "manual"

STEM = os.environ.get("IMAGE_STEM", "sample").strip() or "sample"
CSV_BUCKET = os.environ.get("S3_CSV_BUCKET", "").strip()
LOCAL_CSV = os.environ.get("DESCRIPTIONS_CSV", "").strip()
PORT = int(os.environ.get("PORT", "8000"))

ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "kodefood-vendor-portal-demo")


def _ensure_upload_dir() -> None:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def _safe_ext(filename: str) -> str:
    return Path(filename).suffix.lower()


def list_local_uploads() -> list[dict]:
    _ensure_upload_dir()
    items = []
    for path in sorted(UPLOAD_DIR.iterdir()):
        if path.is_file() and _safe_ext(path.name) in ALLOWED_EXT:
            items.append(
                {
                    "filename": path.name,
                    "url": url_for("uploaded_file", filename=path.name),
                    "status": "pending",
                }
            )
    return items


def load_catalog_rows() -> tuple[list[dict], str]:
    """Return (rows, source_label). Prefer DESCRIPTIONS_CSV, then S3, then sample."""
    if LOCAL_CSV:
        path = Path(LOCAL_CSV)
        if not path.is_file():
            return [], f"missing local file: {LOCAL_CSV}"
        return _parse_csv_text(path.read_text(encoding="utf-8")), f"local:{path}"

    if CSV_BUCKET:
        try:
            import boto3

            key = f"descriptions/{STEM}/descriptions.csv"
            body = (
                boto3.client("s3")
                .get_object(Bucket=CSV_BUCKET, Key=key)["Body"]
                .read()
                .decode("utf-8")
            )
            return _parse_csv_text(body), f"s3://{CSV_BUCKET}/{key}"
        except Exception as exc:  # noqa: BLE001 — demo UI shows the error
            return [], f"S3 error: {exc}"

    if SAMPLE_CSV.is_file():
        return (
            _parse_csv_text(SAMPLE_CSV.read_text(encoding="utf-8")),
            f"sample:{SAMPLE_CSV.name}",
        )
    return [], "no catalog source configured"


def _parse_csv_text(text: str) -> list[dict]:
    reader = csv.DictReader(io.StringIO(text))
    rows = []
    for row in reader:
        uri = (row.get("image_s3_uri") or "").strip()
        desc = (row.get("item_description") or "").strip()
        status = (row.get("photo_status") or "").strip().lower()
        name = uri.rsplit("/", 1)[-1] if uri else ""
        rows.append(
            {
                "image_s3_uri": uri,
                "item_description": desc,
                "photo_status": status,
                "filename": name,
            }
        )
    return rows


def catalog_stats(rows: list[dict]) -> dict:
    accepted = sum(1 for r in rows if r["photo_status"] == "accepted")
    rejected = sum(1 for r in rows if r["photo_status"] == "rejected")
    return {
        "total": len(rows),
        "accepted": accepted,
        "rejected": rejected,
    }


@app.route("/")
def index():
    if MODE == "batch":
        rows, source = load_catalog_rows()
        return render_template(
            "batch.html",
            mode=MODE,
            rows=rows,
            source=source,
            stats=catalog_stats(rows),
            stem=STEM,
        )

    uploads = list_local_uploads()
    submitted = request.args.get("submitted") == "1"
    return render_template(
        "manual.html",
        mode=MODE,
        uploads=uploads,
        submitted=submitted,
    )


@app.route("/upload", methods=["POST"])
def upload():
    if MODE != "manual":
        flash("Uploads are only enabled in MODE=manual.", "error")
        return redirect(url_for("index"))

    _ensure_upload_dir()
    files = request.files.getlist("photos")
    saved = 0
    for f in files:
        if not f or not f.filename:
            continue
        ext = _safe_ext(f.filename)
        if ext not in ALLOWED_EXT:
            continue
        # Keep original stem for demo readability; uuid avoids collisions.
        stem = Path(f.filename).stem[:40]
        dest = UPLOAD_DIR / f"{stem}-{uuid.uuid4().hex[:8]}{ext}"
        f.save(dest)
        saved += 1

    if saved == 0:
        flash("No valid images selected (jpg, jpeg, png, webp, gif).", "error")
        return redirect(url_for("index"))

    flash(f"Uploaded {saved} photo(s). Submit when the order looks right.")
    return redirect(url_for("index"))


@app.route("/submit", methods=["POST"])
def submit():
    if MODE != "manual":
        flash("Submit is only enabled in MODE=manual.", "error")
        return redirect(url_for("index"))

    uploads = list_local_uploads()
    if not uploads:
        flash("Upload at least one photo before submitting.", "error")
        return redirect(url_for("index"))

    return redirect(url_for("index", submitted=1))


@app.route("/clear", methods=["POST"])
def clear():
    if MODE != "manual":
        return redirect(url_for("index"))
    _ensure_upload_dir()
    for path in UPLOAD_DIR.iterdir():
        if path.is_file():
            path.unlink()
    flash("Cleared local uploads.")
    return redirect(url_for("index"))


@app.route("/uploads/<path:filename>")
def uploaded_file(filename: str):
    return send_from_directory(UPLOAD_DIR, filename)


def main() -> None:
    _ensure_upload_dir()
    print(f"KodeFood Vendor Portal — MODE={MODE} on http://0.0.0.0:{PORT}", flush=True)
    app.run(host="0.0.0.0", port=PORT, debug=False)


if __name__ == "__main__":
    main()
