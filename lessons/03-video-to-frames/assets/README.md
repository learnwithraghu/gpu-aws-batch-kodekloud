# Sample Video

Place a short (30–60 second) video file here named `sample.mp4`.

**How to get one:**

Option A — Download a free Creative Commons clip from Pexels:
```bash
# Example: a nature clip (~10 MB)
curl -L "https://www.pexels.com/download/video/854082/" -o sample.mp4
```

Option B — Use `ffmpeg` to generate a test video (no download needed):
```bash
ffmpeg -f lavfi -i testsrc=duration=30:size=640x480:rate=30 \
       -pix_fmt yuv420p sample.mp4
```

Option C — Use any `.mp4` you already have. Keep it under 50 MB for fast uploads.

> **Tip**: The notebook uploads this file to S3 automatically — you don't need to do anything else.
