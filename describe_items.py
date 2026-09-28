"""Write a short food-item description for every photo in one S3 folder.

Vendors upload images (about 25–30 at a time) to the images bucket:

    s3://$S3_BUCKET/$IMAGE_PREFIX/photo.jpg

This job writes one CSV the food app can read:

    s3://$S3_CSV_BUCKET/descriptions/<folder>/descriptions.csv
    columns: image_s3_uri, item_description
"""
import csv
import io
import os

import boto3
import torch
from PIL import Image
from transformers import BlipForConditionalGeneration, BlipProcessor

S3_BUCKET = os.environ["S3_BUCKET"]
S3_CSV_BUCKET = os.environ.get("S3_CSV_BUCKET", S3_BUCKET)
IMAGE_PREFIX = os.environ["IMAGE_PREFIX"].strip("/")
BATCH_SIZE = int(os.environ.get("BATCH_SIZE", "8"))
PROMPT = "a food dish of"

s3 = boto3.client("s3")
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device: {device}")


def list_image_keys() -> list[str]:
    keys = []
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=S3_BUCKET, Prefix=f"{IMAGE_PREFIX}/"):
        for obj in page.get("Contents", []):
            if obj["Key"].lower().endswith((".jpg", ".jpeg", ".png")):
                keys.append(obj["Key"])
    keys.sort()
    return keys


def main():
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained(
        "Salesforce/blip-image-captioning-base"
    ).to(device)
    model.eval()

    keys = list_image_keys()
    print(f"Found {len(keys)} images in s3://{S3_BUCKET}/{IMAGE_PREFIX}/")
    if not keys:
        raise SystemExit("No images to describe.")

    rows = []
    for start in range(0, len(keys), BATCH_SIZE):
        batch_keys = keys[start : start + BATCH_SIZE]
        images = []
        for key in batch_keys:
            body = s3.get_object(Bucket=S3_BUCKET, Key=key)["Body"].read()
            images.append(Image.open(io.BytesIO(body)).convert("RGB"))

        inputs = processor(
            images=images,
            text=[PROMPT] * len(images),
            return_tensors="pt",
        ).to(device)
        with torch.no_grad():
            output_ids = model.generate(**inputs, max_new_tokens=40)
        descriptions = processor.batch_decode(output_ids, skip_special_tokens=True)

        for key, description in zip(batch_keys, descriptions):
            text = description.strip()
            rows.append((f"s3://{S3_BUCKET}/{key}", text))
            print(f"  {key} -> {text}")

    folder = IMAGE_PREFIX.split("/")[-1]
    out_key = f"descriptions/{folder}/descriptions.csv"
    body = io.StringIO()
    writer = csv.writer(body)
    writer.writerow(["image_s3_uri", "item_description"])
    writer.writerows(rows)
    s3.put_object(Bucket=S3_CSV_BUCKET, Key=out_key, Body=body.getvalue().encode())
    print(f"Wrote {len(rows)} descriptions to s3://{S3_CSV_BUCKET}/{out_key}")


if __name__ == "__main__":
    main()
