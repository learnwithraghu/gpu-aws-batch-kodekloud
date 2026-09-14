"""
Lesson 04 — embed_frames.py
Runs INSIDE the Docker container on the AWS Batch GPU instance.

Downloads all frames for a video from S3, runs CLIP on them (GPU),
and stores the embeddings in S3 Vectors.

Environment variables (passed by Batch at submit time):
    S3_BUCKET        — the S3 bucket name
    S3_VECTOR_BUCKET — S3 Vector bucket holding searchable embeddings
    S3_VECTOR_INDEX  — S3 Vector index holding searchable embeddings
    VIDEO_STEM       — video name without extension, e.g. "sample"
    BATCH_SIZE       — how many frames to process at once on GPU (default: 16)

Output:
    One 512-dimension CLIP vector per frame in the configured S3 Vector index.
"""
import io
import json
import os
import boto3
import clip
import numpy as np
import torch
from PIL import Image

from helpers.s3_vectors import frame_vector_record, put_frame_vectors

# ── Config ────────────────────────────────────────────────────────────────────
S3_BUCKET  = os.environ["S3_BUCKET"]
S3_VECTOR_BUCKET = os.environ["S3_VECTOR_BUCKET"]
S3_VECTOR_INDEX = os.environ["S3_VECTOR_INDEX"]
VIDEO_STEM = os.environ["VIDEO_STEM"]         # e.g. "sample"
BATCH_SIZE = int(os.environ.get("BATCH_SIZE", "16"))

s3     = boto3.client("s3")
s3vectors = boto3.client("s3vectors")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device: {DEVICE}")


def load_clip():
    """Load CLIP model onto the GPU."""
    model, preprocess = clip.load("ViT-B/32", device=DEVICE)
    model.eval()   # no gradients needed
    return model, preprocess


def load_frame_manifest() -> list[dict]:
    """Load frame keys and timestamps produced by Lesson 03."""
    key = f"frames/{VIDEO_STEM}/manifest.json"
    obj = s3.get_object(Bucket=S3_BUCKET, Key=key)
    manifest = json.loads(obj["Body"].read())
    print(f"Found {len(manifest)} frames in s3://{S3_BUCKET}/frames/{VIDEO_STEM}/")
    return manifest


def download_frame(key: str) -> Image.Image:
    """Download one JPEG frame from S3 and return as a PIL Image."""
    obj = s3.get_object(Bucket=S3_BUCKET, Key=key)
    return Image.open(io.BytesIO(obj["Body"].read())).convert("RGB")


def embed_all(model, preprocess, frames: list[dict]) -> np.ndarray:
    """Run CLIP image encoder over all frames in batches. Returns (N, 512) array."""
    all_embeddings = []

    for i in range(0, len(frames), BATCH_SIZE):
        batch_frames = frames[i : i + BATCH_SIZE]
        batch_keys   = [frame["frame_key"] for frame in batch_frames]
        batch_images = [preprocess(download_frame(k)) for k in batch_keys]

        # Stack into a single tensor and move to GPU
        batch_tensor = torch.stack(batch_images).to(DEVICE)

        with torch.no_grad():                          # no gradient tracking — saves memory
            features = model.encode_image(batch_tensor)
            features = features / features.norm(dim=-1, keepdim=True)   # normalise to unit length

        all_embeddings.append(features.cpu().numpy())
        print(f"  Embedded frames {i}–{i + len(batch_keys) - 1} / {len(frames)}")

    return np.vstack(all_embeddings).astype("float32")   # shape: (N, 512)


def save_to_s3_vectors(embeddings: np.ndarray, frames: list[dict]):
    """Upsert each embedding with the frame metadata needed for retrieval."""
    records = [
        frame_vector_record(
            VIDEO_STEM,
            frame["frame_key"],
            frame["frame_index"],
            frame["timestamp_ms"],
            embedding,
        )
        for frame, embedding in zip(frames, embeddings, strict=True)
    ]
    count = put_frame_vectors(s3vectors, S3_VECTOR_BUCKET, S3_VECTOR_INDEX, records)
    print(f"Stored {count} embeddings in {S3_VECTOR_BUCKET}/{S3_VECTOR_INDEX}")


def main():
    model, preprocess = load_clip()
    frames            = load_frame_manifest()
    embeddings        = embed_all(model, preprocess, frames)
    save_to_s3_vectors(embeddings, frames)
    print("Done.")


if __name__ == "__main__":
    main()
