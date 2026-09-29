# Video 08 — Demo: check G/VT on-demand quota
**Type:** Demo
**Runtime target:** ~3–4 minutes

---

Okay, so before anyone rewrites the Dockerfile, I want one answer.

A job stuck in RUNNABLE makes people reach for the image. Is this account allowed to launch an on demand g4dn at all? That answer is a service quota.

I'm in the terminal. This lesson only reads. I create nothing. The region is Tokyo, ap-northeast-1. I export AWS_DEFAULT_REGION to ap-northeast-1.

First I describe the compute environment gpu-teaching-gpu-smoke-ce-spot. I want g4dn.xlarge, and minimum vCPUs at zero. Status VALID means Batch accepted the environment. VALID by itself does not mean a GPU will start.

Next I describe the job queue gpu-teaching-gpu-smoke-queue-spot. I want the status, and I want the first compute environment to be that Spot environment. Jobs wait here. The queue does not hold the servers.

Then I describe job definitions, name gpu-teaching-caption-job, status ACTIVE. I take the highest active revision and look at the resource requirements and the job role ARN. Revision one asks for sixteen thousand three hundred eighty-four mebibytes and does not place. Revision two has no job role. Revision three and later place and can write the CSV. I do not create the old example names. gpu-teaching-ce, gpu-teaching-queue, and gpu-teaching-job-def are not resources in this account.

The command this demo is here for comes last. I run aws service-quotas get-service-quota. Service code ec2. Quota code L-DB2E81BA. Region ap-northeast-1. The name I want back is Running On-Demand G and VT instances.

If the value is zero, the on demand environment and queue can look VALID and Healthy while CloudWatch stays empty. In the console I open Service Quotas, Amazon EC2, region ap-northeast-1, Running On-Demand G and VT instances, and I request an increase. At least four vCPUs. This course often asks for eight. Until get-service-quota shows the new value, I stay on the Spot queue.

If the value is four or higher, on demand is permitted. Spot can still be unavailable. The Spot family is a different code, L-3819A6DF, All G and VT Spot Instance Requests. This teaching account uses eight on that one. A job that sits RUNNABLE for several minutes on Spot is almost always no Spot capacity, not a broken image.

The helper helpers/watch_batch_job.sh prints this same quota when a job stays RUNNABLE for about two minutes. Lesson eight uses that helper while you wait.

Lambda and SageMaker are built for other jobs. Why this folder stays on Batch is next.
