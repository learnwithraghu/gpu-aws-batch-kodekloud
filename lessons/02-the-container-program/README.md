# Lesson 02 — The container program

Two short files. Students read them. They do not run a job in this lesson.

| File | Job |
|------|-----|
| [`photos.py`](photos.py) | S3 only: list the folder, download one photo, write one CSV |
| [`describe_items.py`](describe_items.py) | GPU only: load the model, describe a small group, then call `photos.py` |

Batch starts one command: `python /app/describe_items.py`. That file imports `photos.py`. Both are copied into the image in lesson 03.

## How to teach this

About 20 minutes. Open `photos.py` first. Leave the GPU file closed until the S3 story is clear.

### Open with this

A vendor folder is already in S3. This program reads that folder and writes one CSV. It does not create buckets, a registry, or a Batch environment. Those are other lessons.

Draw two boxes:

```
photos.py          describe_items.py
list photos   ←    main()
download one  ←    describe 8 photos on the GPU
write the CSV ←    collect the sentences
```

Say: "The GPU file is the one Batch runs. It asks the S3 file to fetch photos and to save the result."

### Walk `photos.py` (about 5 minutes)

Read top to bottom. Stop on each comment.

1. **The three settings.** `S3_BUCKET`, `S3_CSV_BUCKET`, and `IMAGE_PREFIX` arrive from the job submission. They are not written in the file. `images/sample` is the example.
2. **`list_photo_keys`.** One folder. Keep `.jpg`, `.jpeg`, and `.png`. Sort them so the CSV order does not change between runs. One `list_objects_v2` call covers a normal vendor drop of 25–30 photos.
3. **`download_photo`.** S3 returns bytes. Pillow turns those bytes into a picture the model can see.
4. **`save_csv`.** `images/sample` becomes the folder name `sample`. The object key is `descriptions/sample/descriptions.csv`. Two columns: `image_s3_uri`, `item_description`.

Ask: "Thirty photos. How many CSV files?" Answer: one.

### Walk `describe_items.py` (about 10 minutes)

1. **`device`.** On the `g4dn` this prints `cuda`. If CUDA is missing it prints `cpu` and the job is on the wrong machine.
2. **`load_model`.** A small caption model (`Salesforce/blip-image-captioning-base`) is loaded and moved onto the GPU. `model.eval()` means we are not training.
3. **`describe_group`.** One GPU pass. Every photo in the group gets the same prompt: `a photography of`. The model returns one sentence per photo. `num_beams=3` tries a few wordings. `torch.no_grad()` means we do not store training data. One sentence is enough. Do not open the model.
4. **The loop in `main`.** Draw 30 photos as four groups: 8, 8, 8, 6. Each group is one call to `describe_group`. Eight is GPU memory, not a separate output file.
5. **The last line.** `photos.save_csv(rows)` writes the single file. The groups disappear into that one list of rows.

Ask, and wait for answers:

- Where does `IMAGE_PREFIX` come from? (The job submission, lesson 08. Not this file.)
- Why groups of 8? (So the GPU is not handed the whole folder at once.)
- Which file writes the CSV? (`photos.py`.)
- What command does Batch run? (`python /app/describe_items.py`.)

### Leave out

- How BLIP works inside.
- IAM, Docker, and the job definition. Lessons 03, 07, and 08.
- Training, gradients, and token ids beyond the one `no_grad` sentence.

## What the job receives

| Variable | Meaning | Read in |
|----------|---------|---------|
| `S3_BUCKET` | Images bucket | `photos.py` |
| `S3_CSV_BUCKET` | Bucket that receives the CSV | `photos.py` |
| `IMAGE_PREFIX` | Folder to read, such as `images/sample` | `photos.py` |
| `BATCH_SIZE` | Photos per GPU pass. Default 8 | `describe_items.py` |

The container uses the job role from lesson 01 for the S3 calls.

## Where these files go next

Lesson 03 copies both files into the image, at `/app/photos.py` and `/app/describe_items.py`. Lesson 08 runs `python /app/describe_items.py`. A change to either file is invisible to Batch until the image is built and pushed again.
