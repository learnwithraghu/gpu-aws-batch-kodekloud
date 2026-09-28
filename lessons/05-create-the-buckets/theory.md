# Lesson 05 — Theory

Buckets hold the data. The GPU image holds the program. Batch connects them at job time.

## Object storage for ML I/O

GPU instances are temporary. Disk on the instance disappears when Batch scales in. Photos and the catalog CSV must live somewhere durable and reachable from any new instance.

S3 is that place. The job downloads photos, runs the model, and uploads one CSV. The next vendor drop is just more objects under a prefix — no AMI baking of images required.

## Bucket naming and global uniqueness

S3 bucket names are global across all AWS accounts. `my-photos` is likely taken. Suffixing with your account ID (`gpu-teaching-images-<account-id>`) makes collisions rare and ties the name to the account that owns the course.

The CSV bucket in this account still contains the word `captions` in its name. That is a historical live name. New files use the `descriptions/` prefix inside it.

## Region and location constraint

Create buckets in the same region as Batch (`ap-northeast-1` here). Cross-region traffic adds latency and cost, and some create-bucket calls need an explicit `LocationConstraint` outside `us-east-1`.

Lesson 05’s CLI commands use that constraint for Tokyo. Putting data next to the GPU queue keeps the story simple: one region for the whole pipeline.

## Two buckets vs one

You could put photos and CSVs in one bucket under different prefixes. This course uses two buckets:

- **Images** — vendor uploads; mostly read by the job
- **CSV** — catalog output; written by the job, read by the app

Separate buckets make IAM easier to explain (read on one, write on the other) and make it harder to mix raw uploads with curated catalog files by accident.

## Prefixes are not folders

S3 has flat keys. `images/sample/bowl.jpg` is a string key, not a filesystem folder. Tools and UIs show “folders” by grouping on `/`.

The course still treats `images/<batch>/` as a folder contract: everything the job should see shares that prefix. `list_objects` with that prefix is how `photos.py` finds work. Empty prefix matching is empty work.

## Config in `.env`, secrets elsewhere

Bucket names go in `.env` so CLI lessons and the container env can share them. `.env` is gitignored.

AWS access keys do not belong in `.env` or in the repo. The laptop uses `aws configure` → `~/.aws/`. The container uses the job role. Names are configuration; credentials are identity.
