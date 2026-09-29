# Video 06 — Demo: ECR login and push
**Type:** Demo
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

I'm publishing the local image, because Batch can only pull from ECR. The tag on this laptop is gpu-teaching:latest, from the build in lesson three. Until that tag exists in the registry, the job definition has nothing real to point at.

I'm at the repo root. The AWS CLI is already configured, and the region for this course is Tokyo. I export AWS_DEFAULT_REGION as ap-northeast-1. I set ACCOUNT_ID by running aws sts get-caller-identity, with query Account and output text. That value is your account id. I don't paste the number into the repo. I build REGISTRY from it: your account id, then .dkr.ecr.ap-northeast-1.amazonaws.com. I echo REGISTRY. Healthy output is that host and nothing else. No gpu-teaching on the line, and no tag. If the region inside that string is wrong, every later command talks to the wrong registry.

Next I check whether the repository exists. I run aws ecr describe-repositories, repository-names gpu-teaching, region ap-northeast-1. If the name is already there, I skip creation. This course uses one repository, gpu-teaching. If the command fails with RepositoryNotFoundException, I create it. The command is aws ecr create-repository, repository-name gpu-teaching, image-scanning-configuration scanOnPush=true, region ap-northeast-1. scanOnPush=true is the course default, so ECR can flag known CVEs after the push. I want that set before the layers go up. A second describe-repositories should then show gpu-teaching.

Then I log Docker in. I run aws ecr get-login-password, region ap-northeast-1, and I pipe it to docker login. The username is AWS. The password comes from stdin. The registry argument is the host I just echoed. Healthy output is a login that finishes with no error. The password lasts about twelve hours. If I come back later and Docker says the login expired, I run this same login again. An expired login fails the push even when the image is built and the repository exists.

I tag and I push. docker tag takes gpu-teaching:latest and points it at the full URI, the registry host plus gpu-teaching:latest. docker push takes that full URI. The first push is large, about three point eight gigabytes, because the CUDA and PyTorch layers haven't been uploaded yet. Later pushes send only the layers that changed. A script-only change to photos.py or describe_items.py should move a thin top layer, not the whole three point eight gigabytes. I wait until the push finishes. A denied push here is the expired login or missing push permission. A missing repository shows up here too, which is why I described it first.

I check what ECR stored. I run aws ecr describe-images, repository-name gpu-teaching, image-ids imageTag=latest, region ap-northeast-1. The query asks for imageDetails, the first element, with pushed taken from imagePushedAt and size taken from imageSizeInBytes. Healthy output is a pushed time from this session, and a size in bytes for that multi gigabyte image. If latest didn't land, you won't get those two fields.

If I don't have a .env yet, I copy .env.example to .env. I set ECR_IMAGE_URI to the real registry host, slash, gpu-teaching:latest. I write the expanded host, your account id and ap-northeast-1, so the file doesn't keep an unexpanded shell variable. The job definition in lesson seven points at this URI. A new push of latest is what the next job pulls. A job that already started keeps the image it pulled.

The program is in the registry. The photos and the catalog CSV can't live on the GPU disk. Next we give them two durable buckets in S3.
