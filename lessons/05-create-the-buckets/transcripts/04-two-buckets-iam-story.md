# Video 04 — Two buckets, clearer IAM
**Type:** Theory
**Runtime target:** ~3 minutes

---

Alright. Why two buckets instead of one?

This course uses two buckets, and each one has a job. The images bucket, gpu-teaching-images- plus your account id, takes vendor uploads. The job mostly reads there. The CSV bucket, gpu-teaching-captions-csv- plus your account id, takes the catalog output. The job writes there. The app reads there. Photos go in one. The catalog CSV goes in the other. That CSV is how KodeFood keeps image_s3_uri, item_description, and photo_status for the photos the menu will use.

You could put photos and CSVs in one bucket under different prefixes. S3 would allow it. images/ and descriptions/ can share a bucket name. This course splits them so the permission story stays easy to say out loud. Least privilege is cleaner with two buckets. The job role reads one and writes the other. Read on the images bucket. Write on the CSV bucket. You can explain that in one sentence, and you can review it in one policy without hunting through prefixes to see who is allowed to delete what.

The split also protects the raw files. Two buckets make it harder to mix vendor uploads with curated catalog files by accident. They cut the chance that a cleanup of outputs deletes the raw uploads in the same sweep. If you are wiping generated CSVs, you are in the CSV bucket. The photos stay in the other one.

The sentence to remember uses the real API names. The task may GetObject on images/*, and PutObject on descriptions/* in the CSV bucket. GetObject is the read of each photo. PutObject is the write of the catalog. The images prefix lives with the vendor folder, on the bucket the job mostly reads. The descriptions prefix lives in the captions-named CSV bucket, which you still do not rename. The job writes the catalog there. The app reads the accepted rows there, after the GPU is gone, which is why the write has to land in S3 and not on the instance disk.

Prefixes could still split the data inside one bucket. This course pays for two names anyway. The IAM sentence stays obvious, and a cleanup of outputs stays in the CSV bucket. You can wipe generated catalogs without sweeping the vendor uploads in the same pass.

The names are only useful if the job and the CLI agree on the strings, and if you know that a prefix is a key, not a folder.

That is the next clip.
