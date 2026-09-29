# Video 01 — Inference, not training
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

Training updates a model's weights. You show it many labeled examples, and the weights move. That movement is backpropagation, an optimizer, and a run of epochs. Inference is the other job. The model is already finished. You hand it new inputs, and it returns outputs. In this course each output is a short caption for one dish photo. This course is inference only. You do not fine-tune BLIP. You do not need a training loop, an optimizer, or a labeled dataset. The GPU's job is to run the same forward pass many times, once per photo, in small groups.

That split is why the machines are shaped the way they are. Training wants long GPU runs, a place to store checkpoints, a way to track experiments, and often more than one machine. A vendor catalog wants a smaller shape. A folder arrives. A job runs. A file comes back. Then the GPU can disappear until the next drop. Repeatable jobs, a clear input, a clear output, and scale to zero between drops. That is the AWS Batch shape this course is building toward.

Picture a restaurant group putting a menu on a delivery app. They upload one folder of about twenty-five to thirty dish photos. Merchandisers need one description per photo so they can review the catalog. The pipeline is there to run the finished model on those plates. It is not there to retrain BLIP on them. The same forward pass runs again and again. About eight photos go through together so they fit in GPU memory. Those eight are memory management. The product is still one description per photo, and still one catalog, not eight separate products.

A few neighboring jobs stay outside this course. Fine-tuning. A labeling workflow. A hyperparameter search. A distributed training loop. The weights here stay frozen. A folder is minutes of work, where a training run is weeks.

Put the vendor drop in the order it actually happens. One folder of dish photos arrives, about twenty-five to thirty pictures. The finished model writes one catalog line per photo. The food app reads that file. Between drops, the GPU machine does not stay on. A training setup would hold the GPU for epochs, store checkpoints, and keep notes on which experiment won. This pipeline stores captions. Follow one photo through the forward pass. The picture goes in, BLIP runs, a caption string comes out, and the weights at the end match the weights at the start. The next photo gets that same pass. When memory is tight, about eight photos share a pass. That group is only how the pictures fit. It is still one catalog.

On the screen, two paths sit side by side. The training path shows weights changing across weeks. The inference path shows those weights frozen, and one food-catalog folder finishing in minutes. The highlight stays on the inference path, labeled for the food catalog.

A photo is a large grid of numbers, and a caption is a lot of matrix math on that grid. Why that math prefers a GPU is next.
