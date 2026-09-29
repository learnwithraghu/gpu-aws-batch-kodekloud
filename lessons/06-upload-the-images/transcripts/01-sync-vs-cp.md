# Video 01 — Sync versus copy
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

When a vendor hands you a folder of food photos, two S3 commands look similar and do different work. aws s3 cp copies. You point it at one object and it uploads that object. With the recursive flag it can walk a directory and copy the tree. It is a one-shot copy. It does not ask whether the destination already holds the same bytes. Run it again and it copies again.

aws s3 sync mirrors a local directory onto a prefix. It compares the folder on your machine with the objects already under that prefix, and it uploads only what is new or what changed. Files that already match are skipped. For a vendor drop of about twenty-five to thirty photos, sync is the command you want. You narrow it so only real photos go up. Exclude everything, then include only jpg, jpeg, and png. A README or a spreadsheet sitting in the same folder stays on the laptop.

The difference shows up the second time the vendor writes. The first sync might send thirty photos. Later they send three retakes. Sync compares checksums, sees three files that differ, and uploads those three. The other twenty-seven stay put. Run the same sync again with nothing changed locally, and nothing goes up. A recursive copy of the whole folder would send all thirty every time, overwrite objects that did not change, and make a small correction look like a full republish.

In this course the photos are data. They are not layers inside the container image. You do not rebuild that image because a vendor added pictures. The job lists a prefix in the images bucket when it runs. Sync is how that prefix gets filled. The usual destination is images/sample/, inside the bucket from lesson five. If this batch uses another folder name, you change the word sample and you keep the images/ prefix. Copy is still the right tool when you truly have one object, a single file path someone pasted into chat. The moment the unit of work is a folder of menu photos, you mirror it with sync.

Re-running sync is also how the folder grows without a ceremony. Add three photos to the local directory, run the same command, and only those three keys change in S3. The container program does not need a new image tag for that. It will list whatever is under the prefix on the day the job runs. That is why a catalog pipeline treats upload and rebuild as different days of work. Today is the upload.

On the screen, picture the laptop folder on the left, thirty photos, three of them marked as new retakes. On the right, the S3 prefix. Arrows leave only those three files. The rest sit still, because the bytes already match. That picture is the command. Compare, then upload the difference.

The next clip is the string on the destination. The prefix you sync to and the prefix the job lists have to name the same folder, or the catalog will not see the photos you just uploaded.
