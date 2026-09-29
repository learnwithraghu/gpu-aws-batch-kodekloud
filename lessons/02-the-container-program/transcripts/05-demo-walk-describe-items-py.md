# Video 05 — Demo: walk through describe_items.py
**Type:** Demo
**Runtime target:** ~3–4 minutes

---

Okay. Here's the worker Batch schedules.

I open describe_items.py because this is that worker. Batch runs python /app/describe_items.py. Listing and the CSV stay in photos.py. This file is the GPU part.

The imports are os, torch, BlipForConditionalGeneration and BlipProcessor from transformers, and photos.

GROUP_SIZE reads BATCH_SIZE through os.environ.get, and the default string is 8. Eight fits the T4 on a g4dn.xlarge. PROMPT is the exact string a photography of. MODEL_NAME is Salesforce/blip-image-captioning-base. FOOD_WORDS is a tuple of food terms. A caption that contains one of them can go live. Anything else is rejected. That catches obvious bad uploads. It does not prove the dish matches the menu.

device is the string cuda when torch.cuda.is_available is true, and cpu otherwise. On the Batch GPU machine I want cuda. cpu means this process has no GPU.

load_model builds a BlipProcessor and a BlipForConditionalGeneration, both with from_pretrained on MODEL_NAME. It moves the model onto device, calls model.eval, and returns the processor and the model. We're describing photos, not training.

describe_group is one GPU pass. The processor takes the pictures, and it takes the same PROMPT repeated once per picture, with return_tensors set to pt. The inputs move onto device. Inside torch.no_grad, model.generate runs with max_new_tokens of twenty, num_beams of three, and repetition_penalty of one point two. batch_decode turns the ids into text with skip_special_tokens, and each sentence is stripped.

photo_status takes that sentence and lowercases it. If any food word appears in the text, it returns accepted. Otherwise it returns rejected. No second model. Just a few lines of Python on the caption.

main loads the model, and the first run may download weights from Hugging Face. Then it lists photos with photos.list_photo_keys. If keys is empty, it raises SystemExit with No images to describe. Nothing is written in that case.

The loop steps by GROUP_SIZE. A folder of thirty becomes groups of eight, eight, eight, and six. Each group is downloaded with photos.download_photo, then passed to describe_group. Each key is paired with its sentence. photo_status marks accepted or rejected. The row is an s3 URI, the description, and that status. The groups append into one list named rows.

After the loop, photos.save_csv writes that list once. Rejected rows stay in the file so the reason is visible. The app uses the accepted rows for the menu.

You can see eval and no_grad in the file, and the next clip is why both of them mean inference.
