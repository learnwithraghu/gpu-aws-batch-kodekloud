# Video 02 — Bucket naming
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

S3 bucket names are a single namespace shared by every AWS account in the world. The first creator wins the name. If someone already took my-data, that name is gone for you. my-photos is the same kind of guess, and it's likely already taken. A short friendly name feels available until create-bucket tells you it isn't.

This course avoids that collision by suffixing the name with your account id. The images bucket is gpu-teaching-images-, then your account id. That ending makes collisions rare, and it ties the bucket to the account that owns the course. You'll see that same string in the console and inside IAM ARNs that grant access to the bucket. The name is part of the identity of the resource, not a label you can reuse in another account.

The CSV bucket follows the same pattern, with one historical twist. The live name is gpu-teaching-captions-csv-, then your account id. The word captions is still in that name. That's the live bucket. It's a historical name, and you don't rename live buckets in the middle of the course. Renaming would be a new bucket, a new set of policies, and a broken path for anything that already points at the old name. New files don't fight the old word. They use the descriptions/ prefix inside that same bucket. The name says captions. The prefix says descriptions. Both are true, and you leave the bucket name alone.

You'll set those two strings in the shell as S3_IMAGES_BUCKET and S3_CSV_BUCKET, built from your account id at the moment you create them. The account id comes from your caller identity. It isn't a number you copy out of a sample and commit.

The captions spelling will show up every time you list buckets, and that's expected. When you look for new catalog files, look for the descriptions/ prefix inside gpu-teaching-captions-csv- plus your account id. Don't look for a second bucket whose name has been edited to say descriptions. A rename would be a new global name. Anything that already has the old name in .env would miss it, including the container that writes the CSV. The account id suffix is the uniqueness. The word captions is the history. You leave both in the live name.

my-data and my-photos fail this test for a different reason. They're short, they're guessable, and the first account anywhere in AWS that created them owns them forever. Your account id on the end is what makes gpu-teaching-images- yours to create, and what makes the console and the IAM ARN point at this account instead of a stranger's bucket with a friendly name.

On the screen, treat a bucket name like a handle on a social network. There's one global list. The first person to claim my-data owns my-data. Your handle is longer on purpose. gpu-teaching-images- plus your account id is how this course stays out of someone else's claim. A second handle, gpu-teaching-captions-csv- plus your account id, is the catalog bucket, word captions and all.

Take a name that already exists in another account and it can never become yours. Take the account-id form and the name points at your account in the console and in the ARN. Next we place both buckets in Tokyo, because a bucket in the wrong region still has a fine name and a painful job.
