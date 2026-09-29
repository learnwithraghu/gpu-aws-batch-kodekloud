# Video 08 — Demo: check G/VT on-demand quota
**Type:** Demo
**Runtime target:** ~3–4 minutes

Read this straight through. It is the words for the recording.

---

A job stuck in RUNNABLE makes people rewrite the Dockerfile. Before any of that, I want one answer. Is this account allowed to launch an on demand g4dn at all? That answer is a service quota. It is not the application code.

I'm in the terminal. This lesson only reads. I create nothing. The region is Tokyo, ap-northeast-1. I export AWS_DEFAULT_REGION to ap-northeast-1 so the calls that follow stay in that region.

First I describe the compute environment gpu-teaching-gpu-smoke-ce-spot. The query asks for the name, the status, the type, the instance types, and the minimum and maximum vCPUs. I want the instance type g4dn.xlarge, and I want minimum vCPUs at zero, so the pool can sit empty. Status VALID means Batch accepted the environment. VALID by itself does not mean a GPU will start.

Next I describe the job queue gpu-teaching-gpu-smoke-queue-spot. I want the status, and I want the first compute environment in the order to be that Spot environment. Jobs on this queue wait here. The queue does not hold the servers.

Then I describe job definitions, name gpu-teaching-caption-job, status ACTIVE. I sort by revision and take the last one, the highest active revision. I look at the revision number, the resource requirements, and the job role ARN. Revision one asks for sixteen thousand three hundred eighty-four mebibytes, and that one does not place. Revision two has no job role, so the GPU can start and the first S3 call still fails. Revision three and later are the ones that place and can write the CSV. I do not create the old example names. gpu-teaching-ce, gpu-teaching-queue, and gpu-teaching-job-def are not resources in this account.

The command this demo is here for comes last. I run aws service-quotas get-service-quota. Service code ec2. Quota code L-DB2E81BA. Region ap-northeast-1. The query prints the quota name and the value. The name I want back is Running On-Demand G and VT instances.

If the value is zero, this is the stuck-job story. The on demand environment and queue can look VALID and Healthy. CloudWatch stays empty. No instance starts, so no container starts, so no logs appear. In the console I open Service Quotas, Amazon EC2, region ap-northeast-1, Running On-Demand G and VT instances, and I request an increase. At least four vCPUs. This course often asks for eight, so one g4dn.xlarge fits with headroom. Approval takes time. Until get-service-quota shows the new value, I stay on the Spot queue.

If the value is four or higher, on demand is permitted. It is not a guarantee that capacity is sitting there. Spot can still be the cheaper default, and Spot can still be unavailable. The Spot family is a different code, L-3819A6DF, All G and VT Spot Instance Requests. This teaching account uses eight on that one. A job that sits RUNNABLE for several minutes on Spot is almost always no Spot capacity, not a broken image.

On the screen, the quota value is in large type, with an arrow that reads either on demand fallback okay, or on demand fallback blocked.

The helper helpers/watch_batch_job.sh prints this same quota when a job stays RUNNABLE for about two minutes. Lesson eight uses that helper while you wait, and it is also where you cancel and resubmit, once this value is at least four.

Lambda and SageMaker are built for other jobs. Why this folder stays on Batch is next.
