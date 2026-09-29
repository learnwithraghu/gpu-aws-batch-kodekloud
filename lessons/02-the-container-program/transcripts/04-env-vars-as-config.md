# Video 04 — Environment variables as job config
**Type:** Theory
**Runtime target:** ~3 minutes

---

So, environment variables are how this job gets configured without a rebuild.

An environment variable is a key and a value, a string, injected into the operating system environment of the container. Python reads that environment with os.environ. You can change the strings at submit time, and you don't rebuild the image to do it. The program you walked in photos.py already works that way. The bucket, the CSV bucket, and the folder are read when the process starts. They're not paths written into the source.

Hard-coded buckets and folders break as soon as the account or the vendor changes. This course keeps one image artifact and many runs. Batch injects the catalog settings, and the image stays the caption program.

Lesson eight is where those overrides are set. The names are S3_BUCKET, the images bucket, read in photos.py. S3_CSV_BUCKET, the bucket that receives the CSV, also read in photos.py. If that one is omitted, the code falls back to S3_BUCKET. IMAGE_PREFIX is the folder to read, and the example is images/sample. BATCH_SIZE is the number of photos in one GPU pass. describe_items.py reads it into GROUP_SIZE, and the default is eight when the variable is absent. The same image can describe images/sample today and images/vendor-b tomorrow. You change the prefix on the submit. You don't change the Dockerfile.

BATCH_SIZE is a memory knob. It's the count of photos handed to one forward pass, because a T4 on a g4dn.xlarge shouldn't be given the whole folder at once. It's not a count of output files. A folder of thirty photos with a batch size of eight still produces one CSV with three columns. Eight, eight, eight, and six are passes over the GPU. The container's permission to call S3 comes from the job role in lesson one. That role isn't one of these variables.

IMAGE_PREFIX arrives as a string like images/sample. photos.py strips slashes off the ends, and list_photo_keys puts one slash back so the listing stays inside that folder. BATCH_SIZE arrives as text. The code turns it into an integer and stores it as GROUP_SIZE. Leave it unset and the default is eight. Hand the model all thirty photos in one pass and you can run out of memory or thrash.

The next clip opens describe_items.py, the file Batch actually starts, and follows one folder through the model in those groups of eight.
