"""KodeFood restaurant back office (S3 upload edition).

Staff add dish photos and names, uploading each photo to Amazon S3 so a later
AWS Batch GPU job can pick it up for ML-powered scoring.
"""
from __future__ import annotations

import json
import mimetypes
import os
import re
import shutil
import signal
import uuid
from pathlib import Path

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from flask import Flask, flash, redirect, render_template, request, send_from_directory, url_for

BASE_DIR = Path(__file__).resolve().parent


def _default_sample_dir() -> Path:
    env_dir = os.environ.get("SAMPLE_DIR")
    if env_dir:
        return Path(env_dir)
    for parent in (BASE_DIR, *BASE_DIR.parents):
        candidate = parent / "images"
        if candidate.is_dir():
            return candidate
    return BASE_DIR / "images"


SAMPLE_DIR = _default_sample_dir()
UPLOAD_DIR = Path(os.environ.get("UPLOAD_DIR", str(BASE_DIR / "uploads")))
MANIFEST_FILE = UPLOAD_DIR / "menu.json"
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "8000"))
ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

S3_BUCKET = os.environ.get("S3_BUCKET", "kodefood-menu-uploads-kodekloud")
S3_PREFIX = os.environ.get("S3_PREFIX", "uploads").strip("/")
AWS_REGION = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "ap-northeast-1"

s3_client = boto3.client("s3", region_name=AWS_REGION)

SAMPLES = [
    {"id": "sample-1", "file": "pexels-luana-ribeiro-44057245-31282322.jpg", "label": "Sample 1"},
    {"id": "sample-2", "file": "pexels-ramon-rangel-661975902-34407507.jpg", "label": "Sample 2"},
    {"id": "sample-3", "file": "pexels-thefindipinxels-37287422.jpg", "label": "Sample 3"},
]
SAMPLE_FILES = {item["id"]: item["file"] for item in SAMPLES}

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "kodefood-menu-desk")


def _ensure_dirs() -> None:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def _empty_state() -> dict:
    return {"submitted": False, "items": []}


def _load_state() -> dict:
    _ensure_dirs()
    if not MANIFEST_FILE.is_file():
        return _empty_state()
    try:
        data = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return _empty_state()
    items = []
    for entry in data.get("items", []):
        filename = entry.get("filename", "")
        if filename and (UPLOAD_DIR / filename).is_file():
            items.append(
                {
                    "id": entry.get("id") or filename,
                    "name": entry.get("name") or "",
                    "filename": filename,
                    "s3_key": entry.get("s3_key") or "",
                    "s3_uri": entry.get("s3_uri") or "",
                }
            )
    return {"submitted": bool(data.get("submitted")) and bool(items), "items": items}


def _save_state(state: dict) -> None:
    _ensure_dirs()
    MANIFEST_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def _view_items(state: dict) -> list[dict]:
    rows = []
    for entry in state["items"]:
        rows.append(
            {
                **entry,
                "url": url_for("uploaded_file", filename=entry["filename"]),
            }
        )
    return rows


def _build_filename(item_name: str, ext: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", item_name.lower()).strip("-")[:40]
    suffix = uuid.uuid4().hex[:8]
    return f"{slug}-{suffix}{ext}" if slug else f"{suffix}{ext}"


def _upload_to_s3(local_path: Path, filename: str, item_name: str) -> str:
    s3_key = f"{S3_PREFIX}/{filename}" if S3_PREFIX else filename
    content_type, _ = mimetypes.guess_type(local_path.name)
    extra_args: dict[str, object] = {
        "ContentType": content_type or "application/octet-stream",
    }
    ascii_name = item_name.encode("ascii", "ignore").decode("ascii").strip()
    if ascii_name:
        extra_args["Metadata"] = {"item-name": ascii_name}
    s3_client.upload_file(str(local_path), S3_BUCKET, s3_key, ExtraArgs=extra_args)
    print(f"Uploaded to s3://{S3_BUCKET}/{s3_key}", flush=True)
    return s3_key


def _delete_from_s3(s3_key: str) -> None:
    if not s3_key:
        return
    try:
        s3_client.delete_object(Bucket=S3_BUCKET, Key=s3_key)
    except (BotoCoreError, ClientError):
        pass


@app.route("/")
def index():
    state = _load_state()
    samples = []
    for sample in SAMPLES:
        path = SAMPLE_DIR / sample["file"]
        if path.is_file():
            samples.append(
                {
                    **sample,
                    "url": url_for("sample_file", filename=sample["file"]),
                }
            )
    return render_template(
        "index.html",
        items=_view_items(state),
        submitted=state["submitted"],
        samples=samples,
    )


@app.route("/add", methods=["POST"])
def add_dish():
    state = _load_state()
    if state["submitted"]:
        flash("This update is already with the menu team. Start another update to add more photos.", "error")
        return redirect(url_for("index"))

    name = (request.form.get("item_name") or "").strip()
    sample_id = (request.form.get("sample_id") or "").strip()
    upload = request.files.get("photo")
    has_upload = bool(upload and upload.filename)

    if not name:
        flash("Write the name of the photo before you add it.", "error")
        return redirect(url_for("index"))
    if not has_upload and sample_id not in SAMPLE_FILES:
        flash("Choose a photo, or pick one of the sample photos.", "error")
        return redirect(url_for("index"))

    _ensure_dirs()
    if has_upload:
        ext = Path(upload.filename).suffix.lower()
        if ext not in ALLOWED_EXT:
            flash("Use a JPG, PNG, WEBP, or GIF photo.", "error")
            return redirect(url_for("index"))
        filename = _build_filename(name, ext)
        local_path = UPLOAD_DIR / filename
        upload.save(local_path)
    else:
        source_name = SAMPLE_FILES[sample_id]
        source = SAMPLE_DIR / source_name
        if not source.is_file():
            flash("That sample photo is missing from the images folder.", "error")
            return redirect(url_for("index"))
        filename = _build_filename(name, source.suffix.lower())
        local_path = UPLOAD_DIR / filename
        shutil.copy2(source, local_path)

    try:
        s3_key = _upload_to_s3(local_path, filename, name)
    except (BotoCoreError, ClientError) as exc:
        if local_path.is_file():
            local_path.unlink()
        flash(f"Could not upload photo to S3 bucket '{S3_BUCKET}': {exc}", "error")
        return redirect(url_for("index"))

    state["items"].append(
        {
            "id": uuid.uuid4().hex[:8],
            "name": name,
            "filename": filename,
            "s3_key": s3_key,
            "s3_uri": f"s3://{S3_BUCKET}/{s3_key}",
        }
    )
    _save_state(state)
    flash(f"Uploaded to s3://{S3_BUCKET}/{s3_key}")
    return redirect(url_for("index"))


@app.route("/remove/<item_id>", methods=["POST"])
def remove_dish(item_id: str):
    state = _load_state()
    if state["submitted"]:
        return redirect(url_for("index"))
    kept = []
    for entry in state["items"]:
        if entry["id"] == item_id:
            path = UPLOAD_DIR / entry["filename"]
            if path.is_file():
                path.unlink()
            _delete_from_s3(entry.get("s3_key", ""))
        else:
            kept.append(entry)
    state["items"] = kept
    _save_state(state)
    return redirect(url_for("index"))


@app.route("/update-menu", methods=["POST"])
def update_menu():
    state = _load_state()
    if not state["items"]:
        flash("Add at least one photo and its name before you update the menu.", "error")
        return redirect(url_for("index"))
    state["submitted"] = True
    _save_state(state)
    return redirect(url_for("index"))


@app.route("/reset", methods=["POST"])
def reset():
    _ensure_dirs()
    for path in UPLOAD_DIR.iterdir():
        if path.is_file() and path.name != ".gitkeep":
            path.unlink()
    return redirect(url_for("index"))


@app.route("/uploads/<path:filename>")
def uploaded_file(filename: str):
    return send_from_directory(UPLOAD_DIR, Path(filename).name)


@app.route("/samples/<path:filename>")
def sample_file(filename: str):
    safe = Path(filename).name
    allowed = {item["file"] for item in SAMPLES}
    if safe not in allowed:
        return ("Not found", 404)
    return send_from_directory(SAMPLE_DIR, safe)


def _handle_sigterm(_signum: int, _frame: object) -> None:
    raise SystemExit(0)


def main() -> None:
    signal.signal(signal.SIGTERM, _handle_sigterm)
    _ensure_dirs()
    s3_target = f"s3://{S3_BUCKET}/{S3_PREFIX}/" if S3_PREFIX else f"s3://{S3_BUCKET}/"
    print(f"KodeFood menu desk — http://127.0.0.1:{PORT}", flush=True)
    print(f"Uploading dish photos to {s3_target} ({AWS_REGION})", flush=True)
    app.run(host=HOST, port=PORT, debug=False)


if __name__ == "__main__":
    main()
