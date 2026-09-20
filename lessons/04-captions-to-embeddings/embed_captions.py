"""
Lesson 04 — embed_captions.py
Runs INSIDE the Docker container on the AWS Batch GPU instance.

Downloads the caption manifest for an image batch from S3, embeds each caption
with CLIP's text encoder (GPU), and stores the embeddings in S3 Vectors.

Environment variables (passed by Batch at submit time):
    S3_BUCKET        — the S3 bucket name
    S3_VECTOR_BUCKET — S3 Vector bucket holding searchable embeddings
    S3_VECTOR_INDEX  — S3 Vector index holding searchable embeddings
    IMAGE_BATCH_STEM — image batch name, e.g. "sample"
    BATCH_SIZE       — how many captions to embed at once on GPU (default: 16)

Output:
    One 512-dimension CLIP text embedding per caption in the configured S3
    Vector index.
"""
import json
import os
import boto3
import numpy as np
import torch
from transformers import CLIPModel, CLIPProcessor

from helpers.s3_vectors import caption_vector_record, put_caption_vectors

# ── Config ────────────────────────────────────────────────────────────────────
S3_BUCKET  = os.environ["S3_BUCKET"]
S3_VECTOR_BUCKET = os.environ["S3_VECTOR_BUCKET"]
S3_VECTOR_INDEX = os.environ["S3_VECTOR_INDEX"]
IMAGE_BATCH_STEM = os.environ["IMAGE_BATCH_STEM"]   # e.g. "sample"
BATCH_SIZE = int(os.environ.get("BATCH_SIZE", "16"))

s3     = boto3.client("s3")
s3vectors = boto3.client("s3vectors")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device: {DEVICE}")


def load_clip():
    """Load CLIP's text encoder onto the GPU."""
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(DEVICE)
    model.eval()   # no gradients needed
    return model, processor


def load_caption_manifest() -> list[dict]:
    """Load image keys and captions produced by Lesson 03."""
    key = f"captions/{IMAGE_BATCH_STEM}/manifest.json"
    obj = s3.get_object(Bucket=S3_BUCKET, Key=key)
    manifest = json.loads(obj["Body"].read())
    print(f"Found {len(manifest)} captions in s3://{S3_BUCKET}/captions/{IMAGE_BATCH_STEM}/")
    return manifest


def embed_all(model, processor, entries: list[dict]) -> np.ndarray:
    """Run CLIP's text encoder over all captions in batches. Returns (N, 512) array."""
    all_embeddings = []

    for i in range(0, len(entries), BATCH_SIZE):
        batch_entries  = entries[i : i + BATCH_SIZE]
        batch_captions = [entry["caption"] for entry in batch_entries]

        inputs = processor(text=batch_captions, return_tensors="pt", padding=True, truncation=True).to(DEVICE)

        with torch.no_grad():                          # no gradient tracking — saves memory
            features = model.get_text_features(**inputs)
            features = features / features.norm(dim=-1, keepdim=True)   # normalise to unit length

        all_embeddings.append(features.cpu().numpy())
        print(f"  Embedded captions {i}–{i + len(batch_entries) - 1} / {len(entries)}")

    return np.vstack(all_embeddings).astype("float32")   # shape: (N, 512)


def save_to_s3_vectors(embeddings: np.ndarray, entries: list[dict]):
    """Upsert each embedding with the image/caption metadata needed for retrieval."""
    records = [
        caption_vector_record(
            IMAGE_BATCH_STEM,
            entry["image_key"],
            entry["image_index"],
            entry["caption"],
            embedding,
        )
        for entry, embedding in zip(entries, embeddings, strict=True)
    ]
    count = put_caption_vectors(s3vectors, S3_VECTOR_BUCKET, S3_VECTOR_INDEX, records)
    print(f"Stored {count} embeddings in {S3_VECTOR_BUCKET}/{S3_VECTOR_INDEX}")


def main():
    model, processor = load_clip()
    entries           = load_caption_manifest()
    embeddings        = embed_all(model, processor, entries)
    save_to_s3_vectors(embeddings, entries)
    print("Done.")


if __name__ == "__main__":
    main()
