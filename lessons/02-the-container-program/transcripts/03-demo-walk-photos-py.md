# Video 03 — Demo: walk through photos.py
**Type:** Demo
**Runtime target:** ~3–4 minutes

---

Alright. I open photos.py because this is where the job learns which folder to read and where the one CSV gets written. There's no GPU code in this file. describe_items.py calls three functions from it.

The imports are csv, io, os, boto3, and Image from PIL. Pillow is how bytes become a picture. The caption model isn't imported here.

The three settings sit right under the imports, and they're not hard-coded. Batch fills them in at submit time. BUCKET reads os.environ for S3_BUCKET. That name is required. If it's missing, Python raises KeyError while the file is importing. CSV_BUCKET uses os.environ.get for S3_CSV_BUCKET, and the fallback is BUCKET. PREFIX reads os.environ for IMAGE_PREFIX and calls strip on the slashes. The comment's example is images/sample. These values are injected by the job. They're not secrets stored in Git.

The file then builds one client, boto3.client called with s3.

list_photo_keys is the inventory scan for one vendor folder. It calls list_objects_v2 with Bucket set to BUCKET and Prefix set to PREFIX plus a slash. One call covers a normal drop. S3 returns up to one thousand keys, and a vendor folder here is about twenty-five to thirty photos. A key is kept when the lowercased name ends with .jpg, .jpeg, or .png. Then keys.sort, so the CSV order doesn't change between runs.

download_photo takes one key. get_object uses the same bucket and that key, and Body read gives raw bytes. Image.open wraps them with io.BytesIO, and convert RGB makes a picture later code can hand to the model. That work is on the CPU.

save_csv takes rows. Each row is a triple: image S3 URI, item description, and photo status. The folder name is the last piece of PREFIX. images/sample becomes sample. The object key is descriptions/sample/descriptions.csv. csv.writer writes the header image_s3_uri, item_description, photo_status, then the rows. When a description contains a comma, the writer quotes it. put_object sends those bytes to CSV_BUCKET at that key. The print line reports how many rows were written, how many were accepted, how many were rejected, and the s3 URI.

Thirty photos, one CSV, three columns. Rejected rows stay in the file. This file lists, downloads, and writes. It never loads the model.

Next you'll see why the buckets and the folder are environment variables, so a different vendor doesn't require a new image.
