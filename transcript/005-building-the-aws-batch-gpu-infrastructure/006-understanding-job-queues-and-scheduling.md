# Video 006 — Understanding Job Queues and Scheduling

**Section:** 005 — Building the AWS Batch GPU Infrastructure
**Lecture#:** 006
**Sheet title:** Understanding Job Queues and Scheduling
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 005-006-understanding-job-queues-and-s

---

Compute environments own machines. Job queues own the waiting line. You never submit a caption job “to a GPU” directly — you submit to a queue, and the queue is ordered against one or more compute environments.

A queue has a state — enabled or disabled — and a priority ordering of compute environments. Batch takes runnable jobs from the queue and tries to place them on capacity from those environments in order. For KodeFood we keep it simple: a Spot GPU queue bound to the Spot compute environment is the default path. A separate on-demand queue exists as a fallback when Spot will not place.

Priority between queues matters when several queues share capacity. Higher-priority queues get scheduling preference. Inside one teaching queue with one environment, life is simpler: jobs wait their turn for the single `g4dn.xlarge` the environment is allowed to run under its max vCPUs.

Why separate Spot and on-demand queues instead of one queue with both environments? Operational clarity. When a job sits waiting, you know which capacity story you opted into. You can point lesson scripts at the Spot queue name and only switch the queue when you deliberately want on-demand. Many production Batch shops isolate fleet types the same way — different queues for different cost and availability profiles.

Scheduling is not fair-share magic for our smoke size. It is: is the queue enabled, is there a matching environment with room, and did EC2 actually give you an instance? If any answer is no, the job waits.

That’s the queue’s job — hold work until capacity can take it. Next we define what “the job” means in concrete terms: the GPU job definition that names the image, memory, GPU count, environment variables, and logging.

---

## Further reading (not spoken)

- [AWS Batch: Job queues](https://docs.aws.amazon.com/batch/latest/userguide/job_queues.html) — queue state, priority, CE order
- [AWS Batch: Fair-share scheduling](https://docs.aws.amazon.com/batch/latest/userguide/fair-share-scheduling.html) — when multiple consumers share a queue
- [AWS Batch: Spot vs on-demand](https://docs.aws.amazon.com/batch/latest/userguide/spot_fleet_IAM_role.html) — capacity types behind queues
