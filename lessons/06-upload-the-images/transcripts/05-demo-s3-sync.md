# Video 05 — Demo: sync photos to S3
**Type:** Demo
**Runtime target:** ~3–4 minutes

---

Okay. Let's put a real vendor folder in the bucket.

The photos have to be in the prefix the job will list, before any GPU starts. This clip is the upload, not a container rebuild. New pictures are data. Sync writes the data. The image we already pushed stays the code. KodeFood will caption this folder later into one CSV the app can read.

I am at the root of the course repo. I source the env file so the images bucket name is already in the shell. The variable is S3_BUCKET. The region is Tokyo, ap-northeast-1.

The local folder is photos, in the repo root. About twenty-five to thirty jpeg and png files is a normal drop. If your folder has another name, change the source path. The destination stem in this demo is sample. If the batch uses another stem, change that word and remember it. Lesson eight submits IMAGE_PREFIX with the same stem.

I run aws s3 sync. The source is the photos folder. The destination is the images bucket, prefix images/sample/. I exclude everything, then include only jpg, jpeg, and png. A README stays home. HEIC stays home. That matches the endings photos.py will keep later.

The first run uploads the folder. I run the same sync again on purpose. The second run should upload nothing, because the checksums already match. If I add three retakes and sync a third time, only those three go up.

Then I list. I run aws s3 ls on images/sample/. I want every photo for this batch, about twenty-five to thirty. That list is what one job turns into one CSV. The keys should read images/sample/, then the file name. If I see file names with no images/sample/ in front, they landed at the bucket root, and the job will not see them.

When that happens, I run the organize uploads helper, with stem sample. First I add dry-run. Dry-run prints the moves and copies nothing. If the printed keys are root objects moving into images/sample/, I run the helper again without dry-run. Then I list the prefix one more time.

Healthy looks like this. The list shows only the sample prefix. The endings are jpg, jpeg, or png. I did not run docker build or push to ECR. The container will download these photos when a job is submitted.

Lesson seven is the Batch environment that can pull that container and read this prefix: the compute environment, the queue, and the job definition.
