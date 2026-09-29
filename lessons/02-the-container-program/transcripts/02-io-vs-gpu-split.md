# Video 02 — I/O file vs GPU file
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

This program is two files on purpose. photos.py is the input and output layer. It lists keys in S3, downloads the bytes, turns those bytes into a picture, and writes the CSV. describe_items.py is the compute layer. It loads the caption model, BLIP, runs generate, walks the folder in groups, and calls photos.py for the storage work. Batch still starts one process. The command is python /app/describe_items.py, and that file imports photos. The import is the only bridge. There's no second container and no second job.

The split exists so a failure tells you which story broke. An AccessDenied from S3 shows up in the input and output file, on the list, the download, or the CSV write. That's a permission or a bucket problem. If the GPU is missing, describe_items.py prints cpu, because torch.cuda.is_available came back false. On a g4dn that line should print cuda. cpu means the job landed on the wrong machine. A bad prompt or a bad generate setting shows up in the GPU file, as dull or repeated sentences, while S3 itself succeeded. Different people can own the two files. Data engineering lives in photos.py. The model code lives in describe_items.py. During an incident you open the file that matches the symptom, and the job id is still the same job.

Follow one folder through the call chain. main in describe_items.py loads the model, then calls photos.list_photo_keys for whatever IMAGE_PREFIX the job was given. The loop cuts that list into groups. For each group it calls photos.download_photo on every key, then one GPU pass captions the group. The sentences accumulate in one list of rows. After every group has succeeded, one call to photos.save_csv writes the file. Thirty photos in images/sample become four GPU passes, eight, eight, eight, and six, and those passes disappear into a single CSV. The groups are a memory tactic. They're not extra output files.

You'll see the same shape in a catalog pipeline that separates warehouse scanning from the ranking model. Instacart-style systems do that. One job id, two files. When the scan fails you open the scanning code. When the sentences are wrong you open the model code. You don't treat the whole container as one undifferentiated script.

Picture the arrows the way this lesson draws them. photos.py lists the photos, downloads one, and writes the CSV. describe_items.py owns main. It asks the S3 file to fetch, it describes a group of eight on the GPU, and it collects the sentences. The arrows point from the GPU file back into the S3 file. Batch doesn't call list_photo_keys, download_photo, or save_csv by name. It starts python /app/describe_items.py, and main makes those calls. Thirty photos, one question about the output. How many CSV files? One. The four passes stay inside that single process, and they collapse into the one list save_csv receives.

On the screen, draw two boxes, photos.py and describe_items.py, with one circle around both of them labeled as a single operating system process. Arrows go from main out to list, download, and save, and the GPU work stays inside the describe_items.py box.

The next clip opens photos.py and walks those three functions from the top of the file down to the CSV key.
