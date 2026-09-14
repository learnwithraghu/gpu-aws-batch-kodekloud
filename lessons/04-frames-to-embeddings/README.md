# Lesson 04 — Frames → Embeddings (The GPU Magic)

> **Concepts**: What is CLIP · What are embeddings · GPU batch processing · Why this needs a GPU  
> **AWS needed**: Batch, S3

---

## What Is an Embedding?

An embedding is a list of numbers (a vector) that represents the "meaning" of something.

```
"a dog playing in the park"   →  [0.21, -0.83, 0.44, ..., 0.07]   (512 numbers)
 🖼️ photo of a dog in the park  →  [0.20, -0.81, 0.46, ..., 0.09]   (512 numbers)
```

The magic: **text and images that have similar meaning end up with similar vectors**. This is what CLIP does. You can then compare vectors to find matching content.

---

## What Is CLIP?

CLIP (Contrastive Language–Image Pretraining) is an OpenAI model that was trained to understand both text and images in the same vector space.

- It encodes images → 512-dimensional vectors
- It encodes text → 512-dimensional vectors  
- Same semantic content = vectors that are close together (high cosine similarity)

We use the smallest CLIP variant: **ViT-B/32** (~350 MB). It fits easily in the T4's 16 GB VRAM.

---

## Why GPU Matters Here

CLIP processes images through a Vision Transformer (ViT). Running ViT on one image on CPU takes ~200–500 ms. On GPU it takes ~5 ms. For 200 frames: **CPU ≈ 100 s vs GPU ≈ 1 s.**

The job processes frames in batches of 16 — all 16 images go through the GPU simultaneously.

---

## Output

The job saves a single file: `embeddings/sample/embeddings.npy`

This is a NumPy array of shape `(N_frames, 512)` — one 512-d vector per frame. It also saves `frame_keys.json` (which S3 key each row corresponds to) so we can retrieve frames by index in Lesson 05.

---

## Key Takeaway

> Embeddings are how ML models represent meaning. CLIP puts images and text in the same space.  
> The GPU processes 16 images at once — that's why it's so much faster than CPU.
