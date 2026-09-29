# Video 06 — Demo: create the buckets
**Type:** Demo
**Runtime target:** ~3–4 minutes

---

Next up. Let's create the two buckets.

I am creating the durable homes for the photos and the catalog CSV before anyone uploads a file or submits a job. The GPU instance will not keep either of them. Two buckets, in Tokyo, named so they do not collide with another account. That is where a KodeFood vendor folder will land, and where the accepted and rejected rows will be written later.

I am at the repo root. I export AWS_DEFAULT_REGION as ap-northeast-1. I set ACCOUNT_ID by running aws sts get-caller-identity, query Account, output text. I export S3_IMAGES_BUCKET as gpu-teaching-images-, then that account id. I export S3_CSV_BUCKET as gpu-teaching-captions-csv-, then that same account id. I echo both names before I create anything. The CSV name still says captions. That is the live bucket. I do not rename it. New files will use the descriptions/ prefix inside it.

ap-northeast-1 requires a location constraint. A second create-bucket on a name I already own fails, so I check first. For the images bucket I run aws s3api head-bucket, bucket set to S3_IMAGES_BUCKET. I send the errors to /dev/null, and I use or, so a failure falls through to create. The create is aws s3api create-bucket, bucket set to that same name, region ap-northeast-1, create-bucket-configuration with LocationConstraint set to ap-northeast-1. I run the same pair for the CSV bucket, head-bucket or create-bucket, same region, same LocationConstraint.

If I already own the bucket, head-bucket succeeds and create-bucket does not run. If the bucket is not there, head-bucket fails quietly and create-bucket runs. us-east-1 is the legacy exception that does not need LocationConstraint. We are not in us-east-1.

Then I list. I run aws s3 ls, piped to grep gpu-teaching. Healthy output is two lines: gpu-teaching-images- plus your account id, and gpu-teaching-captions-csv- plus your account id. Both should show Tokyo, ap-northeast-1. Empty is what I want. Nothing has been uploaded yet.

I add these lines to .env, using the same names I just created. AWS_DEFAULT_REGION equals ap-northeast-1. S3_IMAGES_BUCKET equals the images bucket. S3_CSV_BUCKET equals the CSV bucket. S3_BUCKET equals the images bucket again. Lesson six uploads into S3_BUCKET. The container reads S3_BUCKET and writes to S3_CSV_BUCKET. Keys stay out of this file. The laptop already has aws configure under ~/.aws/. The container will use the job role.

The buckets are empty on purpose. Next we look at sync versus cp, and how a mirror puts the JPEGs under images/sample/.
