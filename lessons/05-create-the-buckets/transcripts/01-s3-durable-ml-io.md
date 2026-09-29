# Video 01 — S3 for ML input and output
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

Amazon Simple Storage Service, S3, is a durable object store. An object is a key, plus bytes, plus metadata. S3 is built around an eleven nines durability design goal. It's regional, and you reach it over HTTPS. The calls you'll care about are GetObject, PutObject, and ListObjectsV2.

GPU jobs need that store because Batch instances are ephemeral. Disk on the instance disappears when Batch scales in. The photos and the catalog CSV have to outlive any one EC2 machine. S3 is the system of record for the inputs and for the catalog output. The GPU image holds the program. The buckets hold the data. Batch connects them when the job runs.

The job downloads the photos, runs the model, and uploads one CSV. The next vendor drop is just more objects under a prefix. You don't bake the photos into an AMI. A new instance can be empty and still do the work, because the objects are still in S3.

Here's the path this course uses. The job lists a prefix that looks like s3://gpu-teaching-images-, then your account id, then /images/sample/. It downloads each object. It writes one catalog object at s3://gpu-teaching-captions-csv-, then your account id, then /descriptions/sample/descriptions.csv. The next job may land on a different instance. The same S3 paths still work, because the paths name objects, not a disk that vanished with the last machine.

If you write that CSV only on the container disk, it's gone when the container exits. That's a product failure. The product never gets the catalog. The GPU did the work and threw the result away with the instance.

Without S3, the caption pipeline has nowhere to put the vendor drop. Batch can start a fresh GPU, pull gpu-teaching:latest from ECR, and still have zero photos, because those photos were never a layer in the image. You don't bake a new AMI every time a vendor sends a folder. You add objects under a prefix. The same image reads whatever is there. That's the split you just crossed. ECR holds the program. S3 holds the input and the one CSV the job uploads.

Durability is why the design goal is eleven nines. The instance is allowed to disappear. The keys are not. GetObject fetches a photo onto the worker for the model. PutObject writes the catalog back. ListObjectsV2 is how the job finds the keys under the prefix before the downloads start. If the list is empty, there's nothing to download and nothing to write. The store only helps after the objects have been put there.

On the screen, picture the EC2 instance as a bubble that disappears when Batch scales in. Beside it, S3 stays, a durable cylinder of objects. One arrow carries photos in, GetObject and ListObjectsV2. One arrow carries the catalog CSV out, PutObject. The bubble can be a different machine next time. The cylinder keeps the keys.

The buckets don't exist until you create them, and the names have to be yours across all of AWS. Next we talk about why those names end with your account id, and why the CSV bucket still has the word captions in it.
