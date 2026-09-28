"""Describe every photo in one S3 folder and write one catalog CSV.

Batch runs this file:  python /app/describe_items.py
S3 listing and the CSV live in photos.py. This file is the GPU part.
"""
import os

import torch
from transformers import BlipForConditionalGeneration, BlipProcessor

import photos

# How many photos the GPU sees in one pass. 8 fits the T4 on a g4dn.xlarge.
GROUP_SIZE = int(os.environ.get("BATCH_SIZE", "8"))
PROMPT = "a photography of"
MODEL_NAME = "Salesforce/blip-image-captioning-base"

# "cuda" on the Batch GPU instance. "cpu" only if this file is started with no GPU.
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Device:", device)


def load_model():
    """Load the caption model and move it onto the GPU."""
    processor = BlipProcessor.from_pretrained(MODEL_NAME)
    model = BlipForConditionalGeneration.from_pretrained(MODEL_NAME)
    model = model.to(device)
    model.eval()  # we are describing photos, not training
    return processor, model


def describe_group(processor, model, images):
    """One GPU pass. images is a short list of pictures. Returns one sentence each."""
    inputs = processor(
        images=images,
        text=[PROMPT] * len(images),  # same prompt on every photo in the group
        return_tensors="pt",
    ).to(device)

    # no_grad: do not store training gradients. This job only generates text.
    # Beams try a few wordings; the short cap cuts a rambling tail.
    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=20,
            num_beams=3,
            repetition_penalty=1.2,
        )

    texts = processor.batch_decode(output_ids, skip_special_tokens=True)
    return [text.strip() for text in texts]


def main():
    processor, model = load_model()

    keys = photos.list_photo_keys()
    print(f"Found {len(keys)} images in s3://{photos.BUCKET}/{photos.PREFIX}/")
    if not keys:
        raise SystemExit("No images to describe.")

    rows = []

    # 30 photos become groups of 8, 8, 8, and 6. Each group is one GPU pass.
    for start in range(0, len(keys), GROUP_SIZE):
        group = keys[start : start + GROUP_SIZE]
        images = [photos.download_photo(key) for key in group]
        descriptions = describe_group(processor, model, images)

        for key, description in zip(group, descriptions):
            uri = f"s3://{photos.BUCKET}/{key}"
            rows.append((uri, description))
            print(f"  {key} -> {description}")

    # One folder in, one CSV out. The groups above do not become extra files.
    photos.save_csv(rows)


if __name__ == "__main__":
    main()
