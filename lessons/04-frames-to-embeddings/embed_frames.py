"""
Lesson 04 — embed_frames.py
Runs INSIDE the Docker container on the AWS Batch GPU instance.

Downloads all frames for a video from S3, runs CLIP on them (GPU),
and saves the embeddings back to S3.

Environment variables (passed by Batch at submit time):
    S3_BUCKET    — the S3 bucket name
    VIDEO_STEM   — video name without extension, e.g. "sample"
    BATCH_SIZE   — how many frames to process at once on GPU (default: 16)

Outputs (saved to S3):
    embeddings/<video_stem>/embeddings.npy   — shape (N, 512), float32
    embeddings/<video_stem>/frame_keys.json  — list of S3 keys, one per row
"""
import io
import json
import os
import boto3
import clip
import numpy as np
import torch
from PIL import Image

# ── Config ────────────────────────────────────────────────────────────────────
S3_BUCKET  = os.environ["S3_BUCKET"]
VIDEO_STEM = os.environ["VIDEO_STEM"]         # e.g. "sample"
BATCH_SIZE = int(os.environ.get("BATCH_SIZE", "16"))

s3     = boto3.client("s3")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device: {DEVICE}")


def load_clip():
    """Load CLIP model onto the GPU."""
    model, preprocess = clip.load("ViT-B/32", device=DEVICE)
    model.eval()   # no gradients needed
    return model, preprocess


def list_frame_keys() -> list[str]:
    """Return all frame S3 keys for this video, sorted."""
    prefix = f"frames/{VIDEO_STEM}/"
    resp   = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=prefix)
    keys   = sorted(obj["Key"] for obj in resp.get("Contents", []))
    print(f"Found {len(keys)} frames in s3://{S3_BUCKET}/{prefix}")
    return keys


def download_frame(key: str) -> Image.Image:
    """Download one JPEG frame from S3 and return as a PIL Image."""
    obj = s3.get_object(Bucket=S3_BUCKET, Key=key)
    return Image.open(io.BytesIO(obj["Body"].read())).convert("RGB")


def embed_all(model, preprocess, frame_keys: list[str]) -> np.ndarray:
    """Run CLIP image encoder over all frames in batches. Returns (N, 512) array."""
    all_embeddings = []

    for i in range(0, len(frame_keys), BATCH_SIZE):
        batch_keys   = frame_keys[i : i + BATCH_SIZE]
        batch_images = [preprocess(download_frame(k)) for k in batch_keys]

        # Stack into a single tensor and move to GPU
        batch_tensor = torch.stack(batch_images).to(DEVICE)

        with torch.no_grad():                          # no gradient tracking — saves memory
            features = model.encode_image(batch_tensor)
            features = features / features.norm(dim=-1, keepdim=True)   # normalise to unit length

        all_embeddings.append(features.cpu().numpy())
        print(f"  Embedded frames {i}–{i + len(batch_keys) - 1} / {len(frame_keys)}")

    return np.vstack(all_embeddings).astype("float32")   # shape: (N, 512)


def save_to_s3(embeddings: np.ndarray, frame_keys: list[str]):
    prefix = f"embeddings/{VIDEO_STEM}"

    # Save embeddings.npy
    buf = io.BytesIO()
    np.save(buf, embeddings)
    s3.put_object(Bucket=S3_BUCKET, Key=f"{prefix}/embeddings.npy", Body=buf.getvalue())

    # Save frame_keys.json (maps row index → S3 key)
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=f"{prefix}/frame_keys.json",
        Body=json.dumps(frame_keys).encode(),
    )

    print(f"Saved embeddings ({embeddings.shape}) to s3://{S3_BUCKET}/{prefix}/")


def main():
    model, preprocess = load_clip()
    frame_keys        = list_frame_keys()
    embeddings        = embed_all(model, preprocess, frame_keys)
    save_to_s3(embeddings, frame_keys)
    print("Done.")


if __name__ == "__main__":
    main()
