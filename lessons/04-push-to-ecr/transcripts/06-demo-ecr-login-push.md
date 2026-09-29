# Video 06 — Demo: ECR login and push
**Type:** Demo
**Runtime target:** ~3–4 minutes

---

Next up. Time to log in and push.

I am publishing the local image, because Batch can only pull from ECR. The tag on this laptop is gpu-teaching:latest, from the build in lesson three. Until that tag exists in the registry, KodeFood has no program ready to caption a vendor folder.

I am at the repo root. The AWS CLI is already configured for Tokyo. I export AWS_DEFAULT_REGION as ap-northeast-1. I set ACCOUNT_ID by running aws sts get-caller-identity, with query Account and output text. I do not paste that number into the repo. I build REGISTRY from it: your account id, then .dkr.ecr.ap-northeast-1.amazonaws.com. I echo REGISTRY. Healthy output is that host alone. If the region inside that string is wrong, every later command talks to the wrong registry.

Next I check whether the repository exists. I run aws ecr describe-repositories, repository-names gpu-teaching, region ap-northeast-1. If the name is already there, I skip creation. If the command fails with RepositoryNotFoundException, I create it with aws ecr create-repository, repository-name gpu-teaching, image-scanning-configuration scanOnPush equals true, region ap-northeast-1. scanOnPush equals true is the course default, so ECR can flag known CVEs after the push.

Then I log Docker in. I run aws ecr get-login-password, region ap-northeast-1, and I pipe it to docker login. The username is AWS. The password comes from stdin. The registry argument is the host I just echoed. The password lasts about twelve hours. If Docker later says the login expired, I run this same login again.

I tag and I push. docker tag takes gpu-teaching:latest and points it at the full URI, the registry host plus gpu-teaching:latest. docker push takes that full URI. The first push is large, about three point eight gigabytes. Later pushes send only the layers that changed. A script-only change to photos.py or describe_items.py should move a thin top layer, not the whole image. I wait until the push finishes.

I check what ECR stored with aws ecr describe-images, repository-name gpu-teaching, image-ids imageTag equals latest. The query asks for imagePushedAt and imageSizeInBytes. Healthy output is a pushed time from this session and a multi gigabyte size.

If I do not have a .env yet, I copy .env.example to .env. I set ECR_IMAGE_URI to the expanded registry host, then gpu-teaching:latest. The job definition in lesson seven points at this URI. A new push of latest is what the next job pulls. A job that already started keeps the image it pulled.

The program is in the registry. Next we give the photos and the catalog CSV two durable buckets in S3.
