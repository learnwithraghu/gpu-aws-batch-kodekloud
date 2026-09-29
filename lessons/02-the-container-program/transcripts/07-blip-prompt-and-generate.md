# Video 07 — Prompt and generate settings
**Type:** Theory  
**Runtime target:** ~3–4 minutes

---

**What BLIP does here.** **Conditional generation**: text **prefix** + image → continued caption. Prefix steers tone (product-style description vs random tags).

**Key `generate` concepts.**

- **Greedy** — one token path; fast, can repeat.
- **Beam search (`num_beams`)** — explore alternatives; often better copy.
- **`max_new_tokens`** — cap length.
- **`repetition_penalty`** — reduce loops.

**Example on one sushi photo.** Three caption variants under different settings — show quality difference visually.

Output lands in **`item_description`** — what merchandisers and the app see.

Idempotent overwrite of same CSV key — next.
