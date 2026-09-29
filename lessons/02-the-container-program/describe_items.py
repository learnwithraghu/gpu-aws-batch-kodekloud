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

# A food-like caption means the photo can go live. Anything else is rejected.
# This catches obvious bad uploads. It does not prove the dish matches the menu.
FOOD_WORDS = (
    "food",
    "dish",
    "meal",
    "plate",
    "bowl",
    "pizza",
    "burger",
    "sandwich",
    "noodles",
    "pasta",
    "rice",
    "soup",
    "salad",
    "chicken",
    "beef",
    "fish",
    "sushi",
    "taco",
    "fries",
    "bread",
    "cake",
    "dessert",
    "fruit",
    "vegetable",
    "vegetables",
    "meat",
    "sauce",
    "drink",
    "coffee",
    "tea",
    "ramen",
    "curry",
    "steak",
    "donut",
    "cookie",
    "egg",
    "cheese",
    "ice cream",
    "icecream",
)

# "cuda" on the Batch GPU instance. "cpu" only if this file is started with no GPU.
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Device:", device, flush=True)


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


def photo_status(description):
    """accepted if the caption looks like food, rejected otherwise."""
    text = description.lower()
    if any(word in text for word in FOOD_WORDS):
        return "accepted"
    return "rejected"


def main():
    print("Loading caption model (first run may download weights)…", flush=True)
    processor, model = load_model()
    print("Model ready. Listing photos…", flush=True)

    keys = photos.list_photo_keys()
    print(f"Found {len(keys)} images in s3://{photos.BUCKET}/{photos.PREFIX}/", flush=True)
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
            status = photo_status(description)
            rows.append((uri, description, status))
            print(f"  {key} -> {description} [{status}]")

    # One folder in, one CSV out. The groups above do not become extra files.
    photos.save_csv(rows)


if __name__ == "__main__":
    main()
