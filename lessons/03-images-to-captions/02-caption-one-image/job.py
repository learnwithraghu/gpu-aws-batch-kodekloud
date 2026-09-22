"""
Lesson 03 · Step 02 — caption-one-image (job.py)
Runs INSIDE the Docker container on the Batch GPU instance.

Captions ONE image from S3 with BLIP and prints the caption.
Goal: see a single caption appear before we scale to a whole batch.

Environment variables (passed at submit time):
    S3_BUCKET   — the S3 bucket name
    IMAGE_KEY   — S3 key of one image, e.g. "images/sample/dog.jpg"
"""
import io
import os

import boto3
import torch
from PIL import Image
from transformers import BlipForConditionalGeneration, BlipProcessor

S3_BUCKET = os.environ["S3_BUCKET"]
IMAGE_KEY = os.environ["IMAGE_KEY"]

s3 = boto3.client("s3")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device: {DEVICE}")

# 1. Download the image from S3
obj = s3.get_object(Bucket=S3_BUCKET, Key=IMAGE_KEY)
image = Image.open(io.BytesIO(obj["Body"].read())).convert("RGB")

# 2. Load BLIP — the ~1 GB image-captioning model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
).to(DEVICE)
model.eval()

# 3. Caption it
inputs = processor(images=image, return_tensors="pt").to(DEVICE)
with torch.no_grad():                              # no gradients — saves memory
    output_ids = model.generate(**inputs, max_new_tokens=30)
caption = processor.batch_decode(output_ids, skip_special_tokens=True)[0]

print(f"Image   : s3://{S3_BUCKET}/{IMAGE_KEY}")
print(f"Caption : {caption}")
