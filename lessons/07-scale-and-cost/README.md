# Lesson 07 — Scale & Cost

> **Concepts**: Batch array jobs · Spot pricing · Cost-per-unit calculation · When to use GPU vs CPU  
> **AWS needed**: Batch, S3

---

## What Is an Array Job?

An array job is one job submission that fans out into N parallel copies.
Each copy gets a unique `AWS_BATCH_JOB_ARRAY_INDEX` environment variable (0, 1, 2, …).

```
submit_job(arrayProperties={"size": 5})
  → runs 5 containers simultaneously
  → each reads its index and picks which image batch to process
```

This is how you scale from 1 batch of images to 100 batches without changing your code — just change the array size and provide a list of image prefixes.

---

## Spot Pricing — What You're Actually Paying

`g4dn.xlarge` (NVIDIA T4) Spot price in Tokyo: **$0.16–0.24 / hr** (varies by availability, typically 60–70% cheaper than On-Demand).

| Task | GPU time | Cost |
|------|----------|------|
| Caption a batch of images (20 images) | ~1 min | ~$0.003 |
| Embed captions (20 captions) | ~30 s | ~$0.002 |
| Full pipeline for 1 image batch | ~2 min | ~$0.006 |
| Full pipeline for 5 image batches (array job) | ~2 min (parallel!) | ~$0.030 |

Notice: 5 image batches in parallel takes **the same wall-clock time** as 1 batch — you're just paying for 5 instances simultaneously.

---

## When GPU vs CPU?

| Use GPU when... | Use CPU when... |
|-----------------|-----------------|
| Processing images with a neural net | Tabular data, SQL queries |
| Running BLIP / CLIP / Whisper on large volumes | Anything < 100 images |
| Training a model | Feature engineering, pandas |
| Batch inference at scale | Model explainability (SHAP) |

Rule of thumb: **if your task involves a neural network and you have >1000 items, GPU is worth it.**

---

## Key Takeaway

> Array jobs = horizontal scaling for free. Spot instances = same power at 70% discount.
> Together: caption and embed 100 image batches on GPU for the cost of a coffee.
