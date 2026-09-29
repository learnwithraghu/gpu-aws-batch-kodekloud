# Video 05 — Prefixes and .env
**Type:** Theory
**Runtime target:** ~3 minutes

---

Okay. Let's talk about prefixes and the env file.

A prefix is a string at the front of an object key. images/sample/ is a prefix. It is not a real filesystem folder. S3 is flat. The object images/sample/bowl.jpg is one key, one set of bytes, and metadata. Nothing in the service created a directory called images and another called sample. The slash is a character in the key. Tools and the console simulate folders by grouping keys on that slash. When the UI shows a folder, it is drawing the grouping. The API still sees strings.

The course still treats images/, then a batch name, as a folder contract. Everything the job should see shares that prefix. That is one KodeFood vendor folder. photos.py finds work by listing objects on it. The call is list_objects_v2, with Prefix set to IMAGE_PREFIX. That list is which photos belong to this batch job. An empty match is empty work. The container can start, the GPU can be fine, and the catalog can still be missing because the prefix pointed at no keys. A wrong prefix is the same failure as an empty one.

The bucket names that hold those keys live in .env, so the CLI lessons and the container environment can share them. .env is gitignored. You set AWS_DEFAULT_REGION to ap-northeast-1. You set S3_IMAGES_BUCKET to the images bucket, gpu-teaching-images- plus your account id. You set S3_CSV_BUCKET to the CSV bucket, gpu-teaching-captions-csv- plus your account id. You set S3_BUCKET to the images bucket again. S3_BUCKET is the images bucket. Lesson six uploads into it. The container reads S3_BUCKET and writes to S3_CSV_BUCKET.

Take the sample batch. The prefix string is images/sample/. A photo named bowl.jpg under it is the key images/sample/bowl.jpg. The container reads S3_BUCKET to get the object, and it writes descriptions/sample/descriptions.csv to S3_CSV_BUCKET. That file holds image_s3_uri, item_description, and photo_status. Empty prefix matching means the list returns no keys. You fix the prefix or the upload before you blame the model.

Names are configuration. Credentials are identity. AWS access keys do not belong in .env or in the repo. The laptop uses aws configure under ~/.aws/. The container uses the job role. The laptop and Batch can share the same bucket strings and still use different credentials.

Next you will watch those two buckets get created in Tokyo, with the location constraint on the create call, and you will see the same four names written into .env.
