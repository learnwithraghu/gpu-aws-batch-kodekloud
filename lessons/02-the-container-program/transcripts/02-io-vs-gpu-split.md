# Video 02 — I/O file vs GPU file
**Type:** Theory
**Runtime target:** ~3 minutes

---

Okay, so this program is two files on purpose.

photos.py is the input and output layer. It lists keys in S3, downloads the bytes, turns those bytes into a picture, and writes the CSV. describe_items.py is the compute layer. It loads the caption model, BLIP, runs generate, marks each caption accepted or rejected, walks the folder in groups, and calls photos.py for the storage work. Batch still starts one process. The command is python /app/describe_items.py, and that file imports photos. The import is the only bridge. There's no second container and no second job.

The split exists so a failure tells you which story broke. An AccessDenied from S3 shows up in the I/O file, on the list, the download, or the CSV write. That's a permission or a bucket problem. If the GPU is missing, describe_items.py prints cpu, because torch.cuda.is_available came back false. On a g4dn that line should print cuda. cpu means the job landed on the wrong machine. A bad prompt or a bad generate setting shows up in the GPU file, as dull or repeated sentences, while S3 itself succeeded. During an incident you open the file that matches the symptom, and the job id is still the same job.

Follow one folder through the call chain. main in describe_items.py loads the model, then calls photos.list_photo_keys for whatever IMAGE_PREFIX the job was given. The loop cuts that list into groups. For each group it calls photos.download_photo on every key, then one GPU pass captions the group. Each caption goes through photo_status, which marks accepted or rejected. The rows accumulate in one list. After every group has succeeded, one call to photos.save_csv writes the file. Thirty photos in images/sample become four GPU passes, eight, eight, eight, and six, and those passes disappear into a single CSV. The groups are a memory tactic. They're not extra output files.

photos.py lists, downloads, and writes. describe_items.py owns main. It asks the S3 file to fetch, it describes a group of eight on the GPU, it marks each row, and it collects the sentences. Batch doesn't call those helpers by name. It starts python /app/describe_items.py, and main makes those calls. Thirty photos. How many CSV files? One.

The next clip opens photos.py and walks those three functions from the top of the file down to the CSV key.
