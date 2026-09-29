# Video 03 — Demo: walk through photos.py
**Type:** Demo
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

I open photos.py because this is where the job learns which folder to read and where the one CSV gets written. There's no GPU code in this file. describe_items.py calls three functions from it. I want you to watch configuration come in at the top, and then watch S3 keys become rows.

The docstring says the file finds the photos in S3, downloads one, and saves the catalog CSV. The imports are csv, io, os, boto3, and Image from PIL. Pillow is how bytes become a picture. The caption model isn't imported here.

The three settings sit right under the imports, and they're not hard-coded. Batch fills them in at submit time. BUCKET reads os.environ for S3_BUCKET. That name is required. If it's missing, Python raises KeyError while the file is importing. CSV_BUCKET uses os.environ.get for S3_CSV_BUCKET, and the fallback is BUCKET, so a job that sets only the images bucket still has a place to put the CSV. PREFIX reads os.environ for IMAGE_PREFIX and calls strip on the slashes. The comment's example is images/sample. These values are injected by the job. They're not secrets stored in Git.

The file then builds one client, boto3.client called with s3. Every later call uses that client.

list_photo_keys is the inventory scan for one vendor folder. It calls list_objects_v2 with Bucket set to BUCKET and Prefix set to PREFIX plus a slash. The slash is added back after the strip, so the prefix is a folder boundary. One call covers a normal drop. The comment says S3 returns up to one thousand keys, and a vendor folder here is about twenty-five to thirty photos. The loop reads response.get for Contents, and an empty folder just gives an empty list. A key is kept when the lowercased name ends with .jpg, .jpeg, or .png. Then keys.sort, so the CSV order doesn't change between runs. There's no second page in this function. It returns that sorted list.

download_photo takes one key. get_object uses the same bucket and that key, and Body read gives raw bytes. Image.open wraps them with io.BytesIO, and convert RGB makes a picture later code can hand to the model. That work is on the CPU. The GPU file hasn't run yet.

save_csv takes rows, a list of pairs, image S3 URI and item description. The folder name is the last piece of PREFIX, from a split on the slash. images/sample becomes sample. The object key is descriptions, slash, that folder, slash, descriptions.csv. For the example, that's descriptions/sample/descriptions.csv. csv.writer writes the header image_s3_uri, item_description, then the rows. When a description contains a comma, the writer quotes it, so the file stays one row per photo. put_object sends those bytes to CSV_BUCKET at that key. The print line reports how many descriptions were written and the s3 URI.

I want you to notice the shape. Thirty photos, one CSV. This file lists, downloads, and writes. It never loads the model.

Those three names came from outside the file. Next you'll see why the buckets and the folder are environment variables, so a different vendor doesn't require a new image.
