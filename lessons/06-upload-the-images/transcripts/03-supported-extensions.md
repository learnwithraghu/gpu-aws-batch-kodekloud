# Video 03 — Supported extensions
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

The prefix list is not the final list. photos.py keeps a key only when the name ends in .jpg, .jpeg, or .png. The check is case insensitive, so .JPG and .PNG stay. Everything else is skipped. A gif, a HEIC, a camera RAW file, a README, a text note, a thumbnail with a different ending. No row for that file. No error line for that file. The loop never mentions it.

That silence is the contract, and it is intentional. The catalog is for the photo types vendors actually send for a menu. Jpeg and png. The program is not a converter for every format a phone can produce. HEIC is common on a camera roll and uncommon in the folder a restaurant exports for a website. If the code raised on every extra file, one sidecar note in the folder would fail an otherwise good batch. The filter drops the stranger and describes the rest.

The support ticket this creates is a count that almost matches. Someone synced thirty files and the CSV has twenty-eight descriptions. The job succeeded. The log says it found twenty-eight images. Nothing says the other two were ignored. You look at the prefix and you find two HEIC files sitting beside the jpegs, or a gif the designer dropped in as a logo. Those keys were listed by S3 and then discarded by the extension check. The row count is the number of surviving keys, not the number of objects in the folder.

The sync command in this lesson already tries to keep those extras off S3. Exclude everything, then include only jpg, jpeg, and png. That filter is on the upload. The filter in photos.py is on the read. You want both. A file can still arrive by the console, by a recursive copy that did not use includes, or by a phone export that used a type the include list never named. The job will not warn you. It will write a shorter CSV and exit zero, as long as at least one supported photo remains.

If every file in the folder fails the ending check, the kept list is empty. Same exit as a wrong prefix. The program says no images to describe, and it does not write the CSV. So a folder of only HEIC is a failed job. A folder of jpeg plus two HEIC files is a successful job with a short catalog. The difference is whether any supported key survived.

When the counts disagree, check extensions before you blame the GPU. List the prefix. Read the endings. Compare that count of jpg, jpeg, and png keys with the number of data rows in the CSV. The header is an extra line. The descriptions should match the supported keys, one for one, in sorted order. Sort is part of the same function, so two runs of the same folder come out in the same sequence.

On the screen, show the prefix as a row of file icons. Jpeg and png icons are green and continue into the CSV. HEIC, gif, and a README are gray, with no arrow and no error badge. The gray files are present. The catalog never speaks their names.

Bytes on S3 and memory on the GPU are the next distinction. A small jpeg is not a small tensor.
