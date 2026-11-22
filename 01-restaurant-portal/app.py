"""KodeFood restaurant back office.

Staff add dish photos and names, then send the batch to the menu team.
The team reviews by hand and updates the customer menu within 24 hours.
"""
from __future__ import annotations

import json
import os
import shutil
import uuid
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, send_from_directory, url_for

BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent
SAMPLE_DIR = REPO_ROOT / "images"
UPLOAD_DIR = BASE_DIR / "uploads"
MANIFEST_FILE = UPLOAD_DIR / "menu.json"
PORT = int(os.environ.get("PORT", "8000"))
ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

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


def _store_bytes(src: Path, ext: str) -> str:
    stored = f"{uuid.uuid4().hex[:10]}{ext}"
    shutil.copy2(src, UPLOAD_DIR / stored)
    return stored


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
        filename = f"{uuid.uuid4().hex[:10]}{ext}"
        upload.save(UPLOAD_DIR / filename)
    else:
        source_name = SAMPLE_FILES[sample_id]
        source = SAMPLE_DIR / source_name
        if not source.is_file():
            flash("That sample photo is missing from the images folder.", "error")
            return redirect(url_for("index"))
        filename = _store_bytes(source, source.suffix.lower())

    state["items"].append(
        {
            "id": uuid.uuid4().hex[:8],
            "name": name,
            "filename": filename,
        }
    )
    _save_state(state)
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


def main() -> None:
    _ensure_dirs()
    print(f"KodeFood menu desk — http://127.0.0.1:{PORT}", flush=True)
    app.run(host="127.0.0.1", port=PORT, debug=False)


if __name__ == "__main__":
    main()
