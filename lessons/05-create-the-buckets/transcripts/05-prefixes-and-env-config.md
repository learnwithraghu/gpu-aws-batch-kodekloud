# Video 05 — Prefixes and .env
**Type:** Theory
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

A prefix is a string at the front of an object key. images/sample/ is a prefix. It is not a real filesystem folder. S3 is flat. The object images/sample/bowl.jpg is one key, one set of bytes, and metadata. Nothing in the service created a directory called images and another called sample. The slash is a character in the key. Tools and the console simulate folders by grouping keys on that slash. When the UI shows a folder, it's drawing the grouping. The API still sees strings.

The course still treats images/, then a batch name, then a slash, as a folder contract. Everything the job should see shares that prefix. photos.py finds work by listing objects on it. The call is list_objects_v2, with Prefix set to IMAGE_PREFIX. That list is which photos belong to this batch job. An empty match is empty work. The container can start, the GPU can be fine, and the catalog can still be missing because the prefix pointed at no keys. A wrong prefix is the same failure as an empty one. You listed, and nothing came back.

The bucket names that hold those keys live in .env, so the CLI lessons and the container environment can share them. .env is gitignored. You set AWS_DEFAULT_REGION to ap-northeast-1. You set S3_IMAGES_BUCKET to the images bucket, gpu-teaching-images- plus your account id. You set S3_CSV_BUCKET to the CSV bucket, gpu-teaching-captions-csv- plus your account id. You set S3_BUCKET to the images bucket again. S3_BUCKET is the images bucket. Lesson six uploads into it. The container reads S3_BUCKET and writes to S3_CSV_BUCKET. Same names you created, written down so the next lesson doesn't invent a second pair.

Take the sample batch. The prefix string is images/sample/. A photo named bowl.jpg under it is the key images/sample/bowl.jpg, one string, not a path the disk created. list_objects_v2 with Prefix set to IMAGE_PREFIX returns that key when the upload matched. The container reads S3_BUCKET, the images bucket, to get the object, and it writes descriptions/sample/descriptions.csv to S3_CSV_BUCKET. Empty prefix matching means the list returns no keys. That's empty work. You fix the prefix or the upload before you blame the model.

Names are configuration. Credentials are identity. AWS access keys don't belong in .env, and they don't belong in the repo. The laptop uses aws configure, and those credentials live under ~/.aws/. The container uses the job role. The laptop and Batch can both reference the same bucket strings and still use different credentials. Copying a key into .env to make the container work would break that split. The file is for names. The role is for identity.

On the screen, picture a flat list of keys. One line reads images/sample/bowl.jpg, a single string. The console draws a folder images, then sample, by splitting on the slash. Beside the list, a .env file shows the four lines: the region, the two bucket names, and S3_BUCKET repeating the images bucket. The credentials sit apart from that file, under ~/.aws/ on the laptop and on the job role in the cloud.

Next you'll watch those two buckets get created in Tokyo, with the location constraint on the create call, and you'll see the same four names written into .env.
