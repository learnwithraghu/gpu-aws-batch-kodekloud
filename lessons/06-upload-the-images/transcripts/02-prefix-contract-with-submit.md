# Video 02 — Prefix contract with submit
**Type:** Theory
**Runtime target:** ~3 minutes

---

Okay, so the upload and the submit have to agree on the same folder.

A prefix is the folder string the job is willing to list. In this course that string is IMAGE_PREFIX. The example is images/sample. photos.py reads that variable, strips slashes from the ends, and then lists objects with the prefix plus one slash. So images/sample and images/sample/, in the environment variable, become the same list. The objects themselves still have to live under that folder. Keys look like images/sample/bowl.jpg.

The upload and the submit have to agree on that folder. The sync destination is the images bucket, prefix images/sample/. Lesson eight sets IMAGE_PREFIX to images/sample on the submit call. Same folder. No extra directory in the middle. If this batch uses another stem, both sides change together. Sync to images/vendor-b/, and set IMAGE_PREFIX to images/vendor-b. That is one KodeFood vendor folder in, and one descriptions.csv out later, with image_s3_uri, item_description, and photo_status on each row.

A mismatch is quiet until you read the log. Photos can be visible in the console under images/other/, while the job lists images/sample/. list_objects_v2 only returns keys that start with the prefix it was given. The other folder is invisible. The bucket root is invisible too. A photo uploaded as bowl.jpg, with no images/sample/ in front of it, is not in this list. One list call is enough for a normal vendor drop of twenty-five to thirty photos. The call still returns nothing if the string is wrong.

When the list is empty, describe_items.py prints that it found zero images and exits with the message no images to describe. It does not write the catalog CSV. The job fails fast. The debug is a comparison, not a model bug. Put the sync destination next to the IMAGE_PREFIX value in the submit environment. They should name the same folder. If the console shows the files at the bucket root, they are not in the prefix yet. The upload demo uses a helper to move those root objects into images/sample/. Dry-run prints the moves and copies nothing.

S3 does not have real directories. images/sample/bowl.jpg is one key, a flat string. The console draws a folder because the key contains slashes. You can see a folder named images, open it, and still be in images/other while the job is aimed at images/sample. Read the key, not the icon.

Supported file types are the next filter on that same list. A photo can be in the right prefix and still never become a row.
