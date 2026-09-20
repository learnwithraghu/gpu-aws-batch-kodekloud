# Lesson 05 — Vector Search

> **Concepts**: Cosine similarity · Nearest-neighbour search · Text → Caption matching
> **AWS needed**: S3, S3 Vectors — no Batch job this lesson

---

## How Vector Search Works

We have `N` caption embeddings in an S3 Vector index: each is a 512-dimensional vector.
We have a text query: `"a dog playing in a park"`.

CLIP can encode that text to a 512-d vector too.

S3 Vectors finds which caption vector is closest to the text vector and
returns the image key and caption stored as metadata.

**Closeness metric: cosine similarity**

```
similarity(a, b) = dot(a, b) / (|a| * |b|)
```

Value ranges from -1 (opposite) to +1 (identical). Because our embeddings are already normalised to unit length (done in Lesson 04), this simplifies to:

```
similarity(a, b) = dot(a, b)          # just a dot product
```

S3 Vectors performs this nearest-neighbour search without downloading every
embedding to the notebook.

---

## Why No GPU This Lesson?

CLIP's small text encoder runs locally on CPU. S3 Vectors performs the search,
which keeps the notebook small while using the same managed retrieval pattern
that scales beyond a few hundred images.

---

## What You'll See

You type a query, the notebook shows you the top 3 matching images next to
their generated captions. Try:
- `"outdoor scene with trees"`
- `"close-up of a person"`
- `"a busy street"`

---

## Key Takeaway

> Vector search = "find me the embedding closest to my query embedding."
> No keywords. S3 Vectors returns the matching image key and caption, which
> lets the notebook retrieve the original image from S3.

