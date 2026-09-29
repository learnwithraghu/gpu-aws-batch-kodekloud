# Video 02 — Bucket naming
**Type:** Theory
**Runtime target:** ~3 minutes

---

Okay, so why do those bucket names end with your account id?

S3 bucket names are a single namespace shared by every AWS account in the world. The first creator wins the name. If someone already took my-data, that name is gone for you. my-photos is the same kind of guess, and it is likely already taken. A short friendly name feels available until create-bucket tells you it is not.

This course avoids that collision by suffixing the name with your account id. The images bucket is gpu-teaching-images-, then your account id. That ending makes collisions rare, and it ties the bucket to the account that owns the course. You will see that same string in the console and inside IAM ARNs that grant access to the bucket. For KodeFood, that is where each vendor folder of photos lands before the caption job runs.

The CSV bucket follows the same pattern, with one historical twist. The live name is gpu-teaching-captions-csv-, then your account id. The word captions is still in that name. That is the live bucket. It is a historical name, and you do not rename live buckets in the middle of the course. Renaming would be a new bucket, a new set of policies, and a broken path for anything that already points at the old name. New files do not fight the old word. They use the descriptions/ prefix inside that same bucket. The name says captions. The prefix says descriptions. Both are true, and you leave the bucket name alone. That is where descriptions.csv lands with image_s3_uri, item_description, and photo_status.

You will set those two strings in the shell as S3_IMAGES_BUCKET and S3_CSV_BUCKET, built from your account id at the moment you create them. The account id comes from your caller identity. It is not a number you copy out of a sample and commit.

When you look for new catalog files, look for the descriptions/ prefix inside that captions-named bucket. Do not look for a second bucket renamed to say descriptions. Anything that already has the old name in .env would miss a rename, including the container that writes the CSV. The account id suffix is the uniqueness. The word captions is the history.

my-data and my-photos fail because they are short, guessable, and owned forever by whoever claimed them first. Your account id on the end is what makes the images bucket yours to create.

Next we place both buckets in Tokyo, because a bucket in the wrong region still has a fine name and a painful job.
