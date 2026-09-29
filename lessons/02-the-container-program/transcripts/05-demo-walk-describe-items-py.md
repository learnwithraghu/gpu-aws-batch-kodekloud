# Video 05 — Demo: walk through describe_items.py
**Type:** Demo
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

I open describe_items.py because this is the worker Batch schedules. The docstring says it describes every photo in one S3 folder and writes one catalog CSV, and it says Batch runs python /app/describe_items.py. Listing and the CSV stay in photos.py. This file is the GPU part. I want you to see the import, then the loop, then the single write at the end.

The imports are os, torch, BlipForConditionalGeneration and BlipProcessor from transformers, and photos. That import is the bridge from the last clip.

GROUP_SIZE reads BATCH_SIZE through os.environ.get, and the default string is 8. The comment says eight fits the T4 on a g4dn.xlarge. PROMPT is the exact string a photography of. MODEL_NAME is Salesforce/blip-image-captioning-base.

device is the string cuda when torch.cuda.is_available is true, and cpu otherwise. The next line prints Device and that value. On the Batch GPU machine I want cuda. cpu means this process has no GPU.

load_model builds a BlipProcessor and a BlipForConditionalGeneration, both with from_pretrained on MODEL_NAME. It moves the model onto device, calls model.eval, and returns the processor and the model. The comment on eval says we're describing photos, not training.

describe_group is one GPU pass. The processor takes the pictures, and it takes the same PROMPT repeated once per picture, with return_tensors set to pt. The inputs move onto device. Inside torch.no_grad, model.generate runs with max_new_tokens of twenty, num_beams of three, and repetition_penalty of one point two. batch_decode turns the ids into text with skip_special_tokens, and each sentence is stripped. One sentence per photo. I'm not opening the model internals.

main prints that it's loading the caption model, and that the first run may download weights. Those weights come from Hugging Face for that model id. The download is network and disk on the first cloud run. This clip is only a read of the file on the laptop. After load_model, it prints that the model is ready and lists photos. keys comes from photos.list_photo_keys. It prints how many images it found, with the bucket and the prefix. If keys is empty, it raises SystemExit with the message No images to describe. Nothing is written in that case.

The loop steps by GROUP_SIZE. The comment walks a folder of thirty as groups of eight, eight, eight, and six. Each group is downloaded with photos.download_photo, then passed to describe_group. Each key is paired with its sentence. The row is an s3 URI, built from photos.BUCKET and the key, plus the description. It prints the key and the sentence as it goes. The groups append into one list named rows. They don't become extra files.

After the loop, photos.save_csv writes that list once. The write waits until every group has succeeded.

I want you to notice the order in main, because it's easy to remember backwards. The model loads before the list. The list runs before any download. The downloads happen inside the group loop, not for the whole folder up front. save_csv runs once, after the last group. A first cloud run may spend time on the Hugging Face download before it prints how many images it found. On this laptop we're only reading the source.

You can see eval and no_grad in the file, and the next clip is why both of them mean inference, and what goes wrong if this job behaves like training.
