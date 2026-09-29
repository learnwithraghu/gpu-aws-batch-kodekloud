# Video 01 — Sync versus copy
**Type:** Theory
**Runtime target:** ~3 minutes

---

Hello. Let's talk about sync versus copy.

When a vendor hands you a folder of food photos, two S3 commands look similar and do different work. aws s3 cp copies. You point it at one object and it uploads that object. With the recursive flag it can walk a directory and copy the tree. It is a one-shot copy. It does not ask whether the destination already holds the same bytes. Run it again and it copies again.

aws s3 sync mirrors a local directory onto a prefix. It compares the folder on your machine with the objects already under that prefix, and it uploads only what is new or what changed. Files that already match are skipped. For a vendor drop of about twenty-five to thirty photos, sync is the command you want. You narrow it so only real photos go up. Exclude everything, then include only jpg, jpeg, and png. A README or a spreadsheet stays on the laptop.

The difference shows up the second time. The first sync might send thirty photos. Later they send three retakes. Sync compares checksums, sees three files that differ, and uploads those three. The other twenty-seven stay put. Run the same sync again with nothing changed, and nothing goes up. A recursive copy would send all thirty every time and make a small correction look like a full republish.

In this course the photos are data. They are not layers inside the container image. You do not rebuild because a KodeFood vendor added pictures. The job lists a prefix in the images bucket when it runs. Sync is how that prefix gets filled. The usual destination is images/sample/, inside the bucket from lesson five. If this batch uses another folder name, change the word sample and keep the images/ prefix. Copy is right for one object. For a folder of photos the menu will use, you mirror with sync.

Add three photos, run the same command, and only those three keys change in S3. The container does not need a new image tag. It will list whatever is under the prefix on the day the job runs. Today is the upload.

The next clip is the string on the destination. The prefix you sync to and the prefix the job lists have to name the same folder, or the catalog will not see the photos you just uploaded.
