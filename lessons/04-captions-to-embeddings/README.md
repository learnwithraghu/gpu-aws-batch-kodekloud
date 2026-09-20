# Lesson 04 — Captions → Embeddings (The GPU Magic)

> **Concepts**: What is CLIP · What are embeddings · GPU batch processing · Why this needs a GPU
> **AWS needed**: Batch, S3

---

## What Is an Embedding?

An embedding is a list of numbers (a vector) that represents the "meaning" of something.

```
"a dog playing in the park"           →  [0.21, -0.83, 0.44, ..., 0.07]   (512 numbers)
"a dog running through a field"       →  [0.20, -0.81, 0.46, ..., 0.09]   (512 numbers)
```

The magic: **text with similar meaning ends up with similar vectors**. This is
what CLIP does. You can then compare vectors to find matching content.

---

## What Is CLIP?

CLIP (Contrastive Language–Image Pretraining) is an OpenAI model that was trained to understand both text and images in the same vector space.

- It encodes images → 512-dimensional vectors
- It encodes text → 512-dimensional vectors
- Same semantic content = vectors that are close together (high cosine similarity)

We use the smallest CLIP variant: **ViT-B/32** (~600 MB total). It fits easily in the T4's 16 GB VRAM.

---

## Why Embed Captions Instead of Images?

Lesson 03's BLIP model already converted every image into a natural-language
**caption**. Embedding those captions with CLIP's **text encoder** keeps the
whole pipeline text-first end to end: your search query is text, and what
you're matching against is text (the caption) — so results are driven by
what the image is *about*, in plain language, rather than by raw visual
similarity.

---

## Why GPU Matters Here

CLIP's text encoder is a transformer. Running it one caption at a time on CPU
takes tens of milliseconds; on GPU it's effectively instant. The job embeds
captions in batches of 16 — all 16 go through the GPU simultaneously.

---

## Output

The job upserts one record per caption into the configured S3 Vectors index
(`S3_VECTOR_BUCKET` / `S3_VECTOR_INDEX`). Each record stores the 512-d
embedding plus metadata: `image_key`, `image_index`, `image_batch_stem`, and
the `caption` text itself — everything Lesson 05 needs to show you a match.

---

## Key Takeaway

> Embeddings are how ML models represent meaning. CLIP puts images and text in the same space.
> Here we embed the *caption text*, so search stays purely semantic and language-driven.

