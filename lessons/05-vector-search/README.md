# Lesson 05 — Vector Search

> **Concepts**: Cosine similarity · Nearest-neighbour search · Text → Image matching  
> **AWS needed**: S3 (download only) — no Batch job this lesson

---

## How Vector Search Works

We have `N` frame embeddings: each is a 512-dimensional vector.
We have a text query: `"a dog playing in a park"`.

CLIP can encode that text to a 512-d vector too.

Now it's just math: find which frame vector is closest to the text vector.

**Closeness metric: cosine similarity**

```
similarity(a, b) = dot(a, b) / (|a| * |b|)
```

Value ranges from -1 (opposite) to +1 (identical). Because our embeddings are already normalised to unit length (done in Lesson 04), this simplifies to:

```
similarity(a, b) = dot(a, b)          # just a dot product
```

We compute this for all N frames with one numpy operation and take the top-k.

---

## Why No GPU This Lesson?

Search is fast on CPU. We only have a few hundred frames — that's thousands of multiply-adds, not millions. On a large production index (millions of embeddings) you'd use a vector database (FAISS, pgvector, Pinecone). But for learning, numpy is perfectly fine and keeps things transparent.

---

## What You'll See

You type a query, the notebook shows you the top 3 matching frames as images. Try:
- `"outdoor scene with trees"`
- `"close-up of a person"`
- `"a busy street"`

---

## Key Takeaway

> Vector search = "find me the embedding closest to my query embedding."  
> No keywords. No tags. Just math. This is what powers semantic search, image search, and RAG systems.
