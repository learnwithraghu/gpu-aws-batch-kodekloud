# Video 03 — Region and location constraint
**Type:** Theory
**Runtime target:** ~3 minutes

---

So, a bucket has a region, and that choice shows up in a few places.

A bucket has a region, and that choice shows up in four places. It changes latency when the job reads and writes. It changes data residency, where the bytes live. It changes whether Batch and ECR can reach the objects in the same region. And it changes the bill, because cross-region traffic adds cost.

This course keeps one region for the whole pipeline. Batch is in Tokyo, ap-northeast-1. ECR is in ap-northeast-1. Both buckets belong there too. Putting the photos next to the GPU queue keeps the story simple. When a KodeFood vendor folder is waiting, the shared pool starts a machine that lists, downloads, and uploads without a cross-region hop.

Creating the bucket in Tokyo is a different API call from creating one in us-east-1. Outside us-east-1, create-bucket needs an explicit LocationConstraint. us-east-1 is the default legacy exception. ap-northeast-1 is not that exception. The lesson five commands pass create-bucket-configuration with LocationConstraint set to ap-northeast-1, the same value as AWS_DEFAULT_REGION. The API requires that constraint in Tokyo. The shell region by itself does not replace it.

The region is chosen when the bucket is created. You will see head-bucket first in the demo, because a second create-bucket on a name you already own fails. The constraint is on the create, the time the bucket is born. After that, setting AWS_DEFAULT_REGION in a new shell does not move a bucket that was born elsewhere. A bucket you created in us-west-2 stays in us-west-2 while the queue runs in Tokyo. Same-region with Batch and with ECR means the pull of gpu-teaching:latest and the GetObject of each photo both happen in ap-northeast-1. One region. One pipeline.

Cross-region traffic adds latency and cost even when the bucket names look perfect. The buckets land in us-west-2. Batch stays in Tokyo. Every photo read and every CSV write becomes cross-region egress. The names look right and the queue is healthy, but the data is simply somewhere else. A correct global name in the wrong region is still the wrong bucket for this pipeline.

Next you will see why those two names are two buckets, instead of one bucket with two prefixes.
