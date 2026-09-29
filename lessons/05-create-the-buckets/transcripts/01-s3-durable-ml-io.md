# Video 01 — S3 for ML input and output
**Type:** Theory
**Runtime target:** ~3 minutes

---

Alright. Welcome back. Let's talk about why the photos and the catalog need S3.

Amazon Simple Storage Service, S3, is a durable object store. An object is a key, plus bytes, plus metadata. S3 is built around an eleven nines durability design goal. It is regional, and you reach it over HTTPS. The calls you will care about are GetObject, PutObject, and ListObjectsV2.

GPU jobs need that store because Batch instances are ephemeral. Disk on the instance disappears when Batch scales in. KodeFood does not keep one GPU per vendor, so the photos and the catalog CSV have to outlive any one EC2 machine. S3 is the system of record for the inputs and for the catalog output. The GPU image holds the program. The buckets hold the data. Batch connects them when the job runs.

The job downloads the photos, runs the model, and uploads one CSV. Each row carries image_s3_uri, item_description, and photo_status. Food-like captions land as accepted. Everything else is rejected. The next vendor drop is just more objects under a prefix. You do not bake the photos into an AMI. A new instance can be empty and still do the work, because the objects are still in S3.

Here is the path this course uses. The job lists a prefix that looks like s3://gpu-teaching-images-, then your account id, then /images/sample/. It downloads each object. It writes one catalog object at s3://gpu-teaching-captions-csv-, then your account id, then /descriptions/sample/descriptions.csv. The next job may land on a different instance. The same S3 paths still work, because the paths name objects, not a disk that vanished with the last machine.

If you write that CSV only on the container disk, it is gone when the container exits. The app never gets the accepted rows for the menu. Without S3, Batch can pull gpu-teaching:latest from ECR and still have zero photos, because those photos were never a layer in the image. You add objects under a prefix. The same image reads whatever is there. ECR holds the program. S3 holds the input and the one CSV the job uploads.

GetObject fetches a photo onto the worker. PutObject writes the catalog back. ListObjectsV2 finds the keys under the prefix. If the list is empty, there is nothing to download and nothing to write.

Next we talk about why those bucket names end with your account id, and why the CSV bucket still has the word captions in it.
