# Video 04 — Two buckets, clearer IAM
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

This course uses two buckets, and each one has a job. The images bucket, gpu-teaching-images- plus your account id, takes vendor uploads. The job mostly reads there. The CSV bucket, gpu-teaching-captions-csv- plus your account id, takes the catalog output. The job writes there. The app reads there. Photos go in one. The catalog CSV goes in the other.

You could put photos and CSVs in one bucket under different prefixes. S3 would allow it. images/ and descriptions/ can share a bucket name. This course splits them so the permission story stays easy to say out loud. Least privilege is cleaner with two buckets. The job role reads one and writes the other. Read on the images bucket. Write on the CSV bucket. You can explain that in one sentence, and you can review it in one policy without hunting through prefixes to see who is allowed to delete what.

The split also protects the raw files. Two buckets make it harder to mix vendor uploads with curated catalog files by accident. They cut the chance that a cleanup of outputs deletes the raw uploads in the same sweep. If you're wiping generated CSVs, you're in the CSV bucket. The photos stay in the other one. That's the operational reason, next to the IAM reason.

The sentence to remember uses the real API names. The task may GetObject on images/*, and PutObject on descriptions/* in the CSV bucket. GetObject is the read of each photo. PutObject is the write of the catalog. The star means the objects under that prefix. The images prefix lives with the vendor uploads, on the bucket the job mostly reads. The descriptions prefix lives in the captions-named CSV bucket, which you still don't rename. The job writes the catalog there. The app reads it there, after the GPU is gone, which is why the write has to land in S3 and not on the instance disk.

Prefixes could still split the data inside one bucket. images/* and descriptions/* can share a single global name. This course pays for two names anyway. The IAM sentence stays obvious, read on one bucket and write on the other, and a cleanup of outputs stays in the CSV bucket. You can wipe generated catalogs without sweeping the vendor uploads in the same pass. That's the accidental-deletion story, and it's the reason two buckets are easier to explain than one bucket with a careful prefix policy.

On the screen, picture two buckets side by side. From the job role, a read arrow goes into the images bucket. A write arrow goes into the CSV bucket. Vendor uploads arrive on the left. The app reads the catalog on the right. One role, two directions, two names. If both arrows pointed at one bucket, you'd be back to explaining prefixes inside a single policy, which this lesson is choosing not to do.

The names are only useful if the job and the CLI agree on the strings, and if you know that a prefix is a key, not a folder. That's the next clip.
