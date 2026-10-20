"""KodeFood Vendor Portal.

Modes (env MODE):
  manual  — Upload menu items in order; clicking Process shows:
            "One of your account managers will review this in 24 hours and get back"
  batch   — Show nightly GPU Batch CSV decisions (accepted / rejected)

Optional Batch mode env:
  S3_CSV_BUCKET    — bucket with descriptions/<stem>/descriptions.csv
  IMAGE_STEM       — folder stem (default: sample)
  DESCRIPTIONS_CSV — local CSV path (overrides S3 when set)
"""
from __future__ import annotations

import csv
import io
import json
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
MANIFEST_FILE = UPLOAD_DIR / "menu_items.json"
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


def _human_title(filename: str) -> str:
    stem = Path(filename).stem
    cleaned = stem.replace("_", " ").replace("-", " ").strip()
    return cleaned.title() if cleaned else "Menu Item"


def _load_manifest() -> list[dict]:
    _ensure_upload_dir()
    if MANIFEST_FILE.is_file():
        try:
            data = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
            if isinstance(data, list):
                valid = []
                for entry in data:
                    fname = entry.get("filename", "")
                    if fname and (UPLOAD_DIR / fname).is_file():
                        valid.append(
                            {
                                "id": entry.get("id") or fname,
                                "name": entry.get("name") or _human_title(fname),
                                "price": entry.get("price") or "",
                                "filename": fname,
                            }
                        )
                return valid
        except Exception:  # noqa: BLE001
            pass

    # Fallback: discover any image files in uploads/
    items = []
    for path in sorted(UPLOAD_DIR.iterdir()):
        if path.is_file() and _safe_ext(path.name) in ALLOWED_EXT:
            items.append(
                {
                    "id": path.name,
                    "name": _human_title(path.name),
                    "price": "",
                    "filename": path.name,
                }
            )
    return items


def _save_manifest(items: list[dict]) -> None:
    _ensure_upload_dir()
    MANIFEST_FILE.write_text(json.dumps(items, indent=2), encoding="utf-8")


def list_local_uploads() -> list[dict]:
    raw_items = _load_manifest()
    items = []
    for idx, entry in enumerate(raw_items, start=1):
        items.append(
            {
                "order": idx,
                "id": entry["id"],
                "name": entry["name"],
                "price": entry.get("price", ""),
                "filename": entry["filename"],
                "url": url_for("uploaded_file", filename=entry["filename"]),
            }
        )
    return items


def _save_uploaded_files(files, custom_name: str = "", custom_price: str = "") -> int:
    _ensure_upload_dir()
    items = _load_manifest()
    saved = 0
    valid_files = [
        f for f in files if f and f.filename and _safe_ext(f.filename) in ALLOWED_EXT
    ]
    for idx, f in enumerate(valid_files):
        ext = _safe_ext(f.filename)
        stem = Path(f.filename).stem[:40]
        stored_name = f"{stem}-{uuid.uuid4().hex[:6]}{ext}"
        dest = UPLOAD_DIR / stored_name
        f.save(dest)

        if custom_name and len(valid_files) == 1:
            item_title = custom_name
        elif custom_name and len(valid_files) > 1:
            item_title = f"{custom_name} #{idx + 1}"
        else:
            item_title = _human_title(f.filename)

        items.append(
            {
                "id": stored_name,
                "name": item_title,
                "price": custom_price,
                "filename": stored_name,
            }
        )
        saved += 1

    if saved:
        _save_manifest(items)
    return saved


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
        except Exception as exc:  # noqa: BLE001
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
        return redirect(url_for("index"))

    files = request.files.getlist("photos")
    item_name = (request.form.get("item_name") or "").strip()
    item_price = (request.form.get("item_price") or "").strip()
    action = (request.form.get("action") or "add").strip()

    saved = _save_uploaded_files(files, custom_name=item_name, custom_price=item_price)

    if action == "process":
        uploads = list_local_uploads()
        if not uploads:
            flash("Please upload at least one menu item image before processing.", "error")
            return redirect(url_for("index"))
        return redirect(url_for("index", submitted=1))

    if saved == 0:
        flash("Please select a valid image file (JPG, PNG, WEBP, or GIF).", "error")
        return redirect(url_for("index"))

    return redirect(url_for("index"))


@app.route("/move/<item_id>/<direction>", methods=["POST"])
def move_item(item_id: str, direction: str):
    items = _load_manifest()
    idx = next((i for i, x in enumerate(items) if x["id"] == item_id), None)
    if idx is not None:
        if direction == "up" and idx > 0:
            items[idx - 1], items[idx] = items[idx], items[idx - 1]
            _save_manifest(items)
        elif direction == "down" and idx < len(items) - 1:
            items[idx + 1], items[idx] = items[idx], items[idx + 1]
            _save_manifest(items)
    return redirect(url_for("index"))


@app.route("/remove/<item_id>", methods=["POST"])
def remove_item(item_id: str):
    items = _load_manifest()
    remaining = []
    for entry in items:
        if entry["id"] == item_id:
            fpath = UPLOAD_DIR / entry["filename"]
            if fpath.is_file():
                fpath.unlink()
        else:
            remaining.append(entry)
    _save_manifest(remaining)
    return redirect(url_for("index"))


@app.route("/submit", methods=["POST"])
def submit():
    if MODE != "manual":
        return redirect(url_for("index"))

    uploads = list_local_uploads()
    if not uploads:
        flash("Please upload at least one menu item before clicking Process.", "error")
        return redirect(url_for("index"))

    return redirect(url_for("index", submitted=1))


@app.route("/clear", methods=["POST"])
def clear():
    if MODE != "manual":
        return redirect(url_for("index"))
    _ensure_upload_dir()
    for path in UPLOAD_DIR.iterdir():
        if path.is_file() and path.name != ".gitkeep":
            path.unlink()
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
