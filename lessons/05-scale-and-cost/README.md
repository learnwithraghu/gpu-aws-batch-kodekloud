# Lesson 05 — Scale & Cost

> **Concepts**: Batch array jobs · Spot pricing · Cost-per-unit calculation · When to use GPU vs CPU  
> **AWS needed**: Batch, S3

---

## What Is an Array Job?

An array job is one job submission that fans out into N parallel copies.
Each copy gets a unique `AWS_BATCH_JOB_ARRAY_INDEX` environment variable (0, 1, 2, …).

```
submit_job(arrayProperties={"size": 5})
  → runs 5 containers simultaneously
  → each reads its index and picks which image batch to caption
```

This is how you scale from 1 batch of images to 100 batches without changing
your code — just change the array size and provide a list of image prefixes.

---

## What `submit_array_job.py` Does

1. Saves the list of image prefixes to `s3://<bucket>/config/array_image_prefixes.json`
2. Submits one array job — each element reads its index, picks its image
   prefix, and runs `generate_captions.py` on that batch
3. Polls until every element reaches a terminal state

Run it:

```bash
# Upload extra image batches first (any folders of .jpg/.png):
aws s3 cp images/ s3://<bucket>/images/ --recursive

# One array element per image prefix:
python submit_array_job.py --image-prefixes images/batch01 images/batch02 images/batch03
```

Each element writes its own `s3://<bucket>/captions/<batch-name>/captions.csv`.

---

## Spot Pricing — What You're Actually Paying

`g4dn.xlarge` (NVIDIA T4) Spot price in Tokyo: **$0.16–0.24 / hr** (varies by
availability, typically 60–70% cheaper than On-Demand).

| Task | GPU time | Cost |
|------|----------|------|
| Caption a batch of images (20 images) | ~1 min | ~$0.003 |
| Caption 5 image batches (array job) | ~1 min (parallel!) | ~$0.015 |
| Caption 100 image batches (array job) | ~1 min (parallel!) | ~$0.30 |

Notice: 5 image batches in parallel take **the same wall-clock time** as 1
batch — you're just paying for 5 instances simultaneously.

---

## When GPU vs CPU?

| Use GPU when... | Use CPU when... |
|-----------------|-----------------|
| Processing images with a neural net | Tabular data, SQL queries |
| Running BLIP / Whisper on large volumes | Anything < 100 images |
| Training a model | Feature engineering, pandas |
| Batch inference at scale | Model explainability (SHAP) |

Rule of thumb: **if your task involves a neural network and you have >1000
items, GPU is worth it.**

---

## Key Takeaway

> Array jobs = horizontal scaling for free. Spot instances = same power at
> 70% discount. Together: caption 100 image batches on GPU for the cost of a
> coffee.
