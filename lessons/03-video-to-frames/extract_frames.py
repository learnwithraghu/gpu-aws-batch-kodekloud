"""
Lesson 03 — extract_frames.py
Runs INSIDE the Docker container on the AWS Batch instance.

Reads a video from S3, extracts one frame every N frames,
and uploads the frames as JPEGs back to S3.

Environment variables (passed by Batch at submit time):
    S3_BUCKET   — the S3 bucket name
    VIDEO_KEY   — S3 key of the input video, e.g. "videos/sample.mp4"
    EVERY_N     — extract one frame every N frames (default: 30)
"""
import os
import cv2
import boto3
import tempfile

# ── Config from environment ──────────────────────────────────────────────────
S3_BUCKET = os.environ["S3_BUCKET"]
VIDEO_KEY  = os.environ["VIDEO_KEY"]          # e.g. "videos/sample.mp4"
EVERY_N    = int(os.environ.get("EVERY_N", "30"))

s3 = boto3.client("s3")


def download_video(local_path: str):
    print(f"Downloading s3://{S3_BUCKET}/{VIDEO_KEY} ...")
    s3.download_file(S3_BUCKET, VIDEO_KEY, local_path)
    print("  Done.")


def extract_and_upload(local_path: str) -> int:
    """Extract every Nth frame and upload each as a JPEG to S3."""
    # Derive an output prefix from the video key: "videos/sample.mp4" → "frames/sample"
    video_stem   = os.path.splitext(os.path.basename(VIDEO_KEY))[0]
    output_prefix = f"frames/{video_stem}"

    cap   = cv2.VideoCapture(local_path)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps   = cap.get(cv2.CAP_PROP_FPS)
    print(f"Video: {total} frames at {fps:.1f} fps — extracting every {EVERY_N} frames")

    frame_idx   = 0
    saved_count = 0

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        if frame_idx % EVERY_N == 0:
            # Encode frame to JPEG in memory
            _, buf = cv2.imencode(".jpg", frame)
            s3_key = f"{output_prefix}/frame_{saved_count:05d}.jpg"
            s3.put_object(Bucket=S3_BUCKET, Key=s3_key, Body=buf.tobytes())
            saved_count += 1

        frame_idx += 1

    cap.release()
    print(f"Uploaded {saved_count} frames to s3://{S3_BUCKET}/{output_prefix}/")
    return saved_count


def main():
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        local_path = tmp.name

    download_video(local_path)
    count = extract_and_upload(local_path)
    print(f"Done. {count} frames extracted.")


if __name__ == "__main__":
    main()
