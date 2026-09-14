# Lesson 03 — Video → Frames

> **Concepts**: What is a video frame · OpenCV · S3 I/O from a Batch job  
> **AWS needed**: Batch, S3

---

## What Is a Frame?

A video is just a sequence of images played quickly (24–60 per second). Each image is called a **frame**.

To do anything with a video in ML (search, classify, embed), we first break it into individual frames. Then we process each frame independently — which is exactly the kind of parallel work GPUs are built for.

---

## Why Run Frame Extraction on GPU?

In this lesson, frame extraction itself is done by `cv2` (CPU-based). The GPU is used for the next step (Lesson 04). But we run this job on a GPU instance because:

1. We want a consistent environment across lessons
2. The same instance will do both extraction + embedding in the full pipeline (Lesson 06)
3. Decoding video (H.264) can optionally be hardware-accelerated on NVIDIA GPUs with the right drivers

**Main lesson**: How to read from S3, do work, write back to S3 — the standard Batch I/O pattern.

---

## The S3 Pattern

Every Batch job in this course follows the same I/O pattern:

```
S3 (input)  →  download to /tmp  →  process  →  upload results to S3  →  done
```

The job reads `S3_BUCKET` and `VIDEO_KEY` from environment variables (passed at submit time).

---

## What the Notebook Does

1. Uploads `assets/sample.mp4` (committed in this folder) to S3
2. Submits the extraction job to Batch
3. After the job completes, downloads a few frames from S3 and displays them

---

## Key Takeaway

> The S3 ↔ Batch I/O pattern is the backbone of every lesson. Learn it here and the rest flows naturally.
