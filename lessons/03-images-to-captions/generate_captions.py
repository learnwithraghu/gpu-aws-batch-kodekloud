"""
Lesson 03 — generate_captions.py
Runs INSIDE the Docker container on the AWS Batch instance.

Downloads a batch of images from S3, runs BLIP image captioning on each (GPU),
and uploads a caption manifest back to S3.

Environment variables (passed by Batch at submit time):
    S3_BUCKET     — the S3 bucket name
    IMAGE_PREFIX  — S3 prefix holding the input images, e.g. "images/sample"
    BATCH_SIZE    — how many images to caption at once on GPU (default: 8)
"""
import io
import json
import os

import boto3
import torch
from PIL import Image
from transformers import BlipForConditionalGeneration, BlipProcessor

# ── Config from environment ──────────────────────────────────────────────────
S3_BUCKET    = os.environ["S3_BUCKET"]
IMAGE_PREFIX = os.environ["IMAGE_PREFIX"]     # e.g. "images/sample"
BATCH_SIZE   = int(os.environ.get("BATCH_SIZE", "8"))

s3     = boto3.client("s3")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device: {DEVICE}")


def load_blip():
    """Load the BLIP image-captioning model onto the GPU."""
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(DEVICE)
    model.eval()   # no gradients needed
    return model, processor


def list_image_keys() -> list[str]:
    """List every image object under IMAGE_PREFIX in S3."""
    keys = []
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=S3_BUCKET, Prefix=f"{IMAGE_PREFIX}/"):
        for obj in page.get("Contents", []):
            if obj["Key"].lower().endswith((".jpg", ".jpeg", ".png")):
                keys.append(obj["Key"])
    keys.sort()
    print(f"Found {len(keys)} images in s3://{S3_BUCKET}/{IMAGE_PREFIX}/")
    return keys


def download_image(key: str) -> Image.Image:
    """Download one image from S3 and return as a PIL Image."""
    obj = s3.get_object(Bucket=S3_BUCKET, Key=key)
    return Image.open(io.BytesIO(obj["Body"].read())).convert("RGB")


def caption_all(model, processor, image_keys: list[str]) -> list[dict]:
    """Run BLIP over all images in batches. Returns the caption manifest."""
    manifest = []

    for i in range(0, len(image_keys), BATCH_SIZE):
        batch_keys   = image_keys[i : i + BATCH_SIZE]
        batch_images = [download_image(k) for k in batch_keys]

        inputs = processor(images=batch_images, return_tensors="pt").to(DEVICE)

        with torch.no_grad():                          # no gradient tracking — saves memory
            output_ids = model.generate(**inputs, max_new_tokens=30)

        captions = processor.batch_decode(output_ids, skip_special_tokens=True)

        for index, (key, caption) in enumerate(zip(batch_keys, captions, strict=True)):
            manifest.append({
                "image_key": key,
                "image_index": i + index,
                "caption": caption.strip(),
            })

        print(f"  Captioned images {i}–{i + len(batch_keys) - 1} / {len(image_keys)}")

    return manifest


def upload_manifest(manifest: list[dict]):
    stem = os.path.basename(IMAGE_PREFIX.rstrip("/"))
    key = f"captions/{stem}/manifest.json"
    s3.put_object(Bucket=S3_BUCKET, Key=key, Body=json.dumps(manifest).encode())
    print(f"Uploaded caption manifest to s3://{S3_BUCKET}/{key}")


def main():
    model, processor = load_blip()
    image_keys        = list_image_keys()
    manifest           = caption_all(model, processor, image_keys)
    upload_manifest(manifest)
    print(f"Done. {len(manifest)} images captioned.")


if __name__ == "__main__":
    main()
