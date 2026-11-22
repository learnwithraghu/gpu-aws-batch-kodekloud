# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pillow>=10.0.0",
#     "boto3>=1.35.0",
# ]
# ///
"""Minimal ML menu satisfaction scorer for KodeFood dish photos.

Scores each image on a 1.0-10.0 scale using visual quality features
(brightness, contrast, sharpness) and decides whether it can be used
in the KodeFood app (>= 8.0) or should be rejected (< 8.0).
"""
from __future__ import annotations

import io
import os
import sys
from pathlib import Path

import boto3
from PIL import Image, ImageFilter, ImageStat

THRESHOLD = 8.0
S3_BUCKET = os.environ.get("S3_BUCKET", "kodefood-menu-uploads-kodekloud")
S3_PREFIX = os.environ.get("S3_PREFIX", "uploads").strip("/")
AWS_REGION = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "ap-northeast-1"
DEFAULT_IMAGES_DIR = Path(__file__).resolve().parent.parent / "images"
ALLOWED_EXT = (".jpg", ".jpeg", ".png", ".webp", ".gif")

# Linear model weights (brightness, contrast, sharpness) + bias
WEIGHTS = (3.0, 4.5, 2.5)
BIAS = 1.0


def score_image(img: Image.Image) -> float:
    """Predict a menu satisfaction score from 1.0 to 10.0."""
    gray = img.convert("L").resize((256, 256))
    brightness = min(ImageStat.Stat(gray).mean[0] / 120.0, 1.0)
    contrast = min(ImageStat.Stat(gray).stddev[0] / 60.0, 1.0)
    sharpness = min(ImageStat.Stat(gray.filter(ImageFilter.FIND_EDGES)).mean[0] / 15.0, 1.0)
    raw = WEIGHTS[0] * brightness + WEIGHTS[1] * contrast + WEIGHTS[2] * sharpness + BIAS
    return round(max(1.0, min(10.0, raw)), 1)


def format_result(name: str, score: float) -> str:
    """Return distinct output depending on whether score meets the 8.0 threshold."""
    if score >= THRESHOLD:
        return (
            f"[APPROVED | score {score:.1f}/10] {name} -> "
            f"High menu satisfaction (>= {THRESHOLD:.1f}). Dish photo can be used in the KodeFood app."
        )
    return (
        f"[REJECTED | score {score:.1f}/10] {name} -> "
        f"Low menu satisfaction (< {THRESHOLD:.1f}). Dish photo cannot be used in the app — please upload a brighter, clearer photo."
    )


def load_local_images(folder: Path) -> list[tuple[str, Image.Image]]:
    """Load dish photos from a local folder."""
    if not folder.is_dir():
        return []
    images = []
    for path in sorted(folder.iterdir()):
        if path.is_file() and path.suffix.lower() in ALLOWED_EXT:
            with Image.open(path) as img:
                images.append((path.name, img.convert("RGB")))
    return images


def load_s3_images() -> list[tuple[str, Image.Image]]:
    """List and download dish photos from S3."""
    s3 = boto3.client("s3", region_name=AWS_REGION)
    prefix = f"{S3_PREFIX}/" if S3_PREFIX else ""
    resp = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=prefix)
    keys = sorted(
        obj["Key"]
        for obj in resp.get("Contents", [])
        if obj["Key"].lower().endswith(ALLOWED_EXT)
    )
    images = []
    for key in keys:
        body = s3.get_object(Bucket=S3_BUCKET, Key=key)["Body"].read()
        with Image.open(io.BytesIO(body)) as img:
            images.append((key, img.convert("RGB")))
    return images


def main() -> None:
    use_s3 = "--s3" in sys.argv[1:] or os.environ.get("SOURCE", "").lower() == "s3"
    if use_s3:
        prefix_path = f"{S3_PREFIX}/" if S3_PREFIX else ""
        print(f"Scoring images from s3://{S3_BUCKET}/{prefix_path} ({AWS_REGION})")
        items = load_s3_images()
    else:
        args = [a for a in sys.argv[1:] if a != "--s3"]
        folder = Path(args[0]) if args else DEFAULT_IMAGES_DIR
        print(f"Scoring local images from {folder}")
        items = load_local_images(folder)

    if not items:
        print("No images found to score.")
        return

    approved = 0
    for name, img in items:
        score = score_image(img)
        if score >= THRESHOLD:
            approved += 1
        print(format_result(name, score))

    rejected = len(items) - approved
    print(f"Summary: {approved} approved (>= {THRESHOLD:.1f}), {rejected} rejected (< {THRESHOLD:.1f})")


if __name__ == "__main__":
    main()
