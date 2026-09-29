# Video 06 — Demo: create the buckets
**Type:** Demo
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

I'm creating the durable homes for the photos and the catalog CSV before anyone uploads a file or submits a job. The GPU instance won't keep either of them. Two buckets, in Tokyo, named so they don't collide with another account.

I'm in the terminal, at the repo root. I export AWS_DEFAULT_REGION as ap-northeast-1. I set ACCOUNT_ID by running aws sts get-caller-identity, query Account, output text. That value is your account id. I export S3_IMAGES_BUCKET as gpu-teaching-images-, then that account id. I export S3_CSV_BUCKET as gpu-teaching-captions-csv-, then that same account id. I echo both names before I create anything. The CSV name still says captions. That's the live bucket. I don't rename it. New files will use the descriptions/ prefix inside it.

ap-northeast-1 requires a location constraint. A second create-bucket on a name I already own fails, so I check first. For the images bucket I run aws s3api head-bucket, bucket set to S3_IMAGES_BUCKET. I send the errors to /dev/null, and I use or, so a failure falls through to create. The create is aws s3api create-bucket, bucket set to that same name, region ap-northeast-1, create-bucket-configuration with LocationConstraint set to ap-northeast-1. I run the same pair for the CSV bucket, head-bucket or create-bucket, same region, same LocationConstraint.

Here's the healthy split. If I already own the bucket, head-bucket succeeds and create-bucket doesn't run. If the bucket isn't there, head-bucket fails, the error stays off the screen, and create-bucket runs. A clean create is the healthy output for a new name. If I skip the check and call create-bucket again on a name I already own, that call fails. That's why the head-bucket is in front. I do this once per bucket, images first, then the CSV bucket. Both get the Tokyo location constraint. us-east-1 is the legacy exception that doesn't need it. We are not in us-east-1.

Then I list. I run aws s3 ls, piped to grep gpu-teaching. Healthy output is two lines. One is gpu-teaching-images- plus your account id. The other is gpu-teaching-captions-csv- plus your account id. In the console those buckets are empty, and the region on each is Tokyo, ap-northeast-1. Empty is what I want. Nothing has been uploaded yet.

I read those two lines before I touch .env. If grep returns one line, one bucket is still missing, and I run head-bucket or create-bucket for the name that didn't show up. If grep returns nothing, the names don't contain gpu-teaching, and I don't write a guess into the file. The account id suffix has to be the value from get-caller-identity, the same value already in the shell.

I add these lines to .env, using the same names I just created. AWS_DEFAULT_REGION equals ap-northeast-1. S3_IMAGES_BUCKET equals the images bucket. S3_CSV_BUCKET equals the CSV bucket. S3_BUCKET equals the images bucket again. S3_BUCKET is the images bucket. Lesson six uploads into it. The container reads S3_BUCKET and writes to S3_CSV_BUCKET. Keys stay out of this file. The laptop already has aws configure under ~/.aws/. The container will use the job role.

The buckets are empty on purpose. Next we look at sync versus cp, and how a mirror puts the JPEGs under the images prefix, images/sample/.
