# Video 03 — Supported extensions
**Type:** Theory
**Runtime target:** ~3 minutes

---

Alright. Not every file in that folder becomes a row.

The prefix list is not the final list. photos.py keeps a key only when the name ends in .jpg, .jpeg, or .png. The check is case insensitive, so .JPG and .PNG stay. Everything else is skipped. A gif, a HEIC, a RAW file, a README. No row. No error line. The loop never mentions it.

That silence is intentional. The catalog is for photo types vendors send for a menu. Jpeg and png. The program is not a converter for every phone format. HEIC is common on a camera roll and uncommon in a restaurant export. If the code raised on every extra file, one sidecar note would fail an otherwise good batch. The filter drops the stranger and describes the rest. Surviving rows still become accepted or rejected once the caption model runs. The app uses the accepted ones for the photos the menu will use.

The support ticket is a count that almost matches. Someone synced thirty files and the CSV has twenty-eight descriptions. The job succeeded. The log says it found twenty-eight images. Nothing says the other two were ignored. You look at the prefix and find two HEIC files, or a gif dropped in as a logo. Those keys were listed by S3 and discarded by the extension check. The row count is surviving keys, not every object in the folder.

Sync already tries to keep extras off S3. Exclude everything, then include only jpg, jpeg, and png. That filter is on the upload. The filter in photos.py is on the read. You want both. A file can still arrive by the console or by a recursive copy that skipped the includes. The job will not warn you. It writes a shorter CSV and exits zero if at least one supported photo remains.

If every file fails the ending check, the kept list is empty. Same exit as a wrong prefix. The program says no images to describe, and it does not write the CSV. Only HEIC is a failed job. Jpeg plus two HEIC files is a successful job with a short catalog.

When counts disagree, check extensions before you blame the GPU. Compare jpg, jpeg, and png keys with the data rows in the CSV. They should match one for one, in sorted order.

Bytes on S3 and memory on the GPU are next. A small jpeg is not a small tensor.
