# Video 06 — Inference mode, not training
**Type:** Theory
**Runtime target:** ~3 minutes

---

Next up. This job describes photos. It doesn't learn new weights.

Two lines in describe_items.py lock that in. model.eval switches layers that behave differently during training, such as dropout and batchnorm, over to inference behavior. torch.no_grad turns off the autograd graph for a forward-only pass. You want both. eval changes how those layers run. no_grad changes what PyTorch stores while they run.

Training builds that graph because a backward pass needs it. Backpropagation walks the graph to compute gradients, and an optimizer would then step the weights. A caption job never does that step. There's no optimizer in this file and no loss. The weights from Salesforce/blip-image-captioning-base stay frozen. Skipping the graph saves memory and time on the T4, which is the same reason the folder is already cut into groups of eight. The GPU is holding the model and a handful of photos. It doesn't also need a training graph for every token.

You can see the two lines in the order the file runs them. load_model moves the network onto device, then calls model.eval. describe_group wraps model.generate in a with torch.no_grad block. The ids that come out of generate are decoded into the sentence. Nothing in that block updates the model. photo_status then marks that sentence accepted or rejected. That check is Python on the text. It is not a weight update either.

Leave the job in training mode and the catalog work gets worse in two ways. Dropout stays random, so the same photo can yield a different sentence for no product reason. The graph is still built, so memory goes up on a card that was already sized for a group of eight. The product ask is a description and a status in the CSV, not a new checkpoint.

model.eval stays on for the rest of the process. You call it once, in load_model, after model.to. Every later group reuses that mode. torch.no_grad is only the block around generate. generate returns token ids. batch_decode runs after the block, with skip_special_tokens, and strip cleans each sentence. Decoding isn't a weight update.

A training script in this spot would name a loss and an optimizer. None of those names are in the file. from_pretrained loads the frozen BLIP weights, eval sets inference behavior, no_grad wraps generate, and the new object you expect in S3 is the CSV from save_csv.

Next you'll see how the prompt and the generate settings choose the sentence that lands in the CSV.
