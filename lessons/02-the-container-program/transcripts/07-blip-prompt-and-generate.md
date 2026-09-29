# Video 07 — Prompt and generate settings
**Type:** Theory
**Runtime target:** ~3 minutes

---

Alright. Let's talk about the prompt and generate settings.

BLIP, in this course, does conditional generation. You give it a short text prefix and a photo, and it continues the prefix while it looks at the image. The prefix steers the tone. A photography-style prefix pushes the model toward a descriptive sentence. A looser prefix drifts toward tags. You don't need the BLIP paper to use it. The contract you care about is the prompt plus the generate arguments, and the sentence those produce in the CSV.

The prompt in describe_items.py is the exact string a photography of. describe_group doesn't invent a new prompt per photo. It builds a list by repeating that string once for every image in the group. A group of eight is the same prefix eight times, paired with eight pictures, in one processor call. return_tensors is pt, and those tensors move onto the same device as the model.

generate then continues each prefix. Greedy decoding is the default one-beam path. At each step it takes the single best next token. It's fast, and it can repeat itself or sound dull. This course doesn't leave it there. num_beams is three, so beam search tries several wordings and keeps a stronger one. max_new_tokens is twenty, a short cap so the model doesn't ramble. repetition_penalty is one point two, which discourages the same phrase looping. After generate, batch_decode reads the token ids with skip_special_tokens turned on, and strip cleans the sentence. That cleaned string is what gets stored, and what photo_status reads to mark accepted or rejected.

Take one sushi photo from a vendor folder. A single greedy path can lock onto a short repeated phrase. Three beams give the model room to pick a fuller descriptive sentence that still starts from a photography of. The cap of twenty new tokens cuts a caption that would have wandered past what a catalog cell can use. You're choosing which wording survives into the row.

That wording is the item_description column, next to image_s3_uri and photo_status. The app reads the accepted rows. The quality of the catalog is the quality of that cell.

Beam search with three beams is what this file actually runs. Greedy is the one-beam default you're not using. The sentence that survives is still one string per photo, stripped, ready for the row.

Next you'll see why every successful run for the same folder writes the same object key, and why a run that fails leaves the previous file in place.
