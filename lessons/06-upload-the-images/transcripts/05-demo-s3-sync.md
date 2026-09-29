# Video 05 — Demo: sync photos to S3
**Type:** Demo
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

The photos have to be in the prefix the job will list, before any GPU starts. This clip puts a real vendor-style folder there. This clip is the upload, not a container rebuild. New pictures are data. Sync writes the data. The image we already pushed stays the code.

I am in the terminal, at the root of the course repo. I source the env file so the images bucket name is already in the shell. The variable is S3_BUCKET. The region for this account is Tokyo, ap-northeast-1, and the CLI is already aimed there.

The local folder is photos, in the repo root. About twenty-five to thirty jpeg and png files is a normal drop. If your folder has another name, you change the source path. The destination stem in this demo is sample. If the batch uses another stem, you change that word in the destination and you remember it. Lesson eight has to submit IMAGE_PREFIX with the same stem.

I run aws s3 sync. The source is the photos folder. The destination is the images bucket, prefix images/sample/. I exclude everything, then include only jpg, jpeg, and png. Those three types are the only objects that go up. A README in the local folder stays home. HEIC stays home. That matches the endings photos.py will keep later.

The first run uploads the folder. I run the same sync again, on purpose. The second run should upload nothing, because the checksums already match. That is the checksum mirror from the theory clip. If I add three retakes and sync a third time, only those three go up.

Then I list. I run aws s3 ls on that same prefix, images/sample/. I want every photo for this batch on that list, and I want the count in the range of about twenty-five to thirty. That list is what one job turns into one CSV. The keys should read images/sample/, then the file name. If I see the file names with no images/sample/ in front of them, they landed at the bucket root, and the job will not see them.

When that happens, I do not re-sync over the top and hope. I run the organize uploads helper, with stem sample. First I add dry-run. Dry-run prints the moves and copies nothing. I read the printed keys. If they are root objects moving into images/sample/, I run the helper again without dry-run. Then I list the prefix one more time.

Healthy looks like this. The list shows only the sample prefix. The endings are jpg, jpeg, or png. The console folder view shows that same folder, which is the string IMAGE_PREFIX will use, images/sample. I did not run docker build. I did not push to ECR. The container does not contain these photos. It will download them when a job is actually submitted.

Lesson seven is the Batch environment that can pull that container and read this prefix: the compute environment, the queue, and the job definition. The photos can sit in S3 until those three exist.
