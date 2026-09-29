# Lesson 02 — Theory

Read this beside [`photos.py`](photos.py) and [`describe_items.py`](describe_items.py). You do not submit a job in this lesson.

## What runs inside the container

AWS Batch starts a command inside a container image. For this course that command is `python /app/describe_items.py`.

The copy of the script on your laptop is only the source. After lesson 04, Batch runs whatever was baked into ECR at `/app/`. Editing the laptop file does nothing until you rebuild and push again.

## Separation of I/O and model code

| File | Responsibility |
|------|----------------|
| `photos.py` | List S3 keys, download bytes, write the CSV |
| `describe_items.py` | Load the model, run the GPU, call `photos.py` |

That split keeps two stories readable. S3 failures and IAM show up in the I/O file. CUDA, prompts, and generate settings show up in the GPU file. Batch still starts one process; imports connect the two.

## Environment variables as job config

Buckets, folder prefix, and group size are not hard-coded paths in the scripts. They arrive as environment variables when the job is submitted (`S3_BUCKET`, `S3_CSV_BUCKET`, `IMAGE_PREFIX`, `BATCH_SIZE`).

The same image can describe `images/sample/` today and `images/vendor-b/` tomorrow without a rebuild. Only the submit override changes. Lesson 08 sets those values.

## GPU memory and micro-batches

A T4 has limited memory. Loading BLIP and then handing it all 30 photos at once can run out of memory or thrash.

The loop takes groups of 8 (default `BATCH_SIZE`). Thirty photos become 8 + 8 + 8 + 6. Each group is one GPU pass. The results append to one list. At the end, one CSV is written. Micro-batches are a memory tactic, not a product split.

## Inference vs training mode

`model.eval()` tells PyTorch layers that behave differently in training (such as dropout) to run in inference mode. `torch.no_grad()` skips building the graph used for backpropagation.

There is no optimizer and no loss. The job only generates text. That is cheaper in memory and matches “describe photos,” not “learn new weights.”

## Prompted captioning (BLIP)

BLIP can take a short text prefix and continue it while looking at the image. This course uses a photography-style prefix so captions are steered toward a descriptive sentence.

`generate` settings matter:

- **Greedy** (default one beam) takes the single best next token each step; it can repeat or sound dull.
- **Beam search** (`num_beams=3`) tries several wordings and keeps a stronger one.
- **`max_new_tokens`** caps length so the model does not ramble.
- **`repetition_penalty`** discourages the same phrase looping.

You do not need the BLIP paper to teach this. Students only need: prompt + generate args → the sentence in the CSV.

## Accept or reject from the caption

After generate, `photo_status` marks each caption `accepted` or `rejected`. A food-like sentence accepts the photo. A caption about a car, a selfie, or a logo rejects it. That is a few lines of Python on the caption text. It is not a second model, and it does not prove the dish matches the menu. Rejected rows stay in the CSV so the reason is visible. KodeFood uses the accepted rows for the menu.

## Idempotent outputs

The output key is derived from the input prefix. `images/sample` becomes `descriptions/sample/descriptions.csv`.

Columns are `image_s3_uri`, `item_description`, and `photo_status`.

A second successful run for the same folder overwrites the same object. That is a product choice: the catalog always reflects the latest successful job for that stem. Failed runs should not leave a half-written contract; this job writes the CSV after all photos are described.
