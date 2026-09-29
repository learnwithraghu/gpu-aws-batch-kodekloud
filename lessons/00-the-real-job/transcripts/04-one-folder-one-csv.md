# Video 04 — One folder, one CSV
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

A good batch job has a contract. One input location. One output object. In this course the input is a prefix in the images bucket, images, then the folder name. That folder name is the batch. The commands in this course use the folder sample. Only jpg, jpeg, and png files are described. The output is one object in the CSV bucket, descriptions, then the same folder name, then descriptions.csv. One job writes that one file.

The contract exists so the rest of the product can trust a path. A mobile menu, or a CMS, integrates against a stable key. It should not have to hunt for whatever file the GPU felt like writing. Operations can alert when that object is missing. They do not have to parse an ambiguous log to learn whether the catalog is there.

Inside the GPU, the model sees photos in groups of about eight, because that is what fits in GPU memory. Those groups are not extra files. Eight photos processed together still append rows to the same CSV. The food app reads that CSV. It does not read the image folder.

Say the keys the way you would find them in the bucket. Input, images bucket, then images, then sample, then a file such as bowl.jpg. Output, CSV bucket, then descriptions, then sample, then descriptions.csv. The batch name in the input prefix and the batch name in the output prefix are the same string. Change the folder, and both sides move together. Leave the folder as sample, and there is still exactly one CSV.

You can already see what a successful file has to contain. The columns are image_s3_uri and item_description. A row for the sample folder might point at the full URI for images/sample/bowl.jpg and carry the sentence, a food dish of noodles with vegetables. One photo, one row. A folder of about twenty-five to thirty supported photos should become that many rows in the same file. The groups of eight never become eight catalog files. Run sample again and the job still owes you that one object, descriptions, then sample, then descriptions.csv, with one row for each jpg, jpeg, or png in the folder. A container can exit zero and still leave the app with nothing useful, if that object is missing, the columns are wrong, or a supported photo has no row.

Success in this course is the file itself. The object has to exist. The schema has to be that pair of columns. There has to be one row per supported photo.

On the screen, one folder icon points at one CSV icon. The loops of eight are drawn inside the GPU box. A single arrow leaves that box and lands on the CSV.

The app treats that file as the product it reads. What those rows are for, and which three AWS services hold the photos, the program, and the run, is next.
