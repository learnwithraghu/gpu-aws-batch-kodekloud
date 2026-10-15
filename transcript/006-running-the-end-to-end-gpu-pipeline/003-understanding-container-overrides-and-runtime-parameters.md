# Video 003 — Understanding Container Overrides and Runtime Parameters

**Section:** 006 — Running the End-to-End GPU Pipeline
**Lecture#:** 003
**Sheet title:** Understanding Container Overrides and Runtime Parameters
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 006-003-understanding-container-overri

---

Why do container overrides exist at all?

Because in production, the team wants to keep the heavy execution contract stable while changing only the small details of each run.

Think about the KodeFood case. The kind of work stays the same every time. We still want the same container, the same broad resource profile, and the same general behavior. What changes from run to run is the specific vendor folder, and sometimes a few runtime values that shape how that one job behaves.

That is the real purpose of overrides. They let one reusable job definition serve many pieces of work.

This is a very common company pattern. Do not rebuild the whole execution setup every time a new input arrives. Keep the platform contract steady, then pass in just the values that identify the current job.

That also keeps the system easier to reason about. If one run succeeds and another run does not, you can ask a focused question: did the environment change, or did only the runtime input change?

There is still a boundary here. Small runtime values are good candidates for overrides. Core resource decisions are not something you should casually change per run, because that can alter placement behavior and create a different operational problem.

So the big idea is this: keep the execution environment stable, and vary the work through runtime input.

Next, we talk about another source of confusion in GPU pipelines: the delay between correct submission and visible execution.

---

## Further reading (not spoken)

- [AWS Batch: Container overrides](https://docs.aws.amazon.com/batch/latest/APIReference/API_ContainerOverrides.html) — command and environment overrides
- [AWS Batch: SubmitJob environment](https://docs.aws.amazon.com/batch/latest/APIReference/API_SubmitJob.html) — runtime parameters on submit
- [Twelve-Factor App: Config](https://12factor.net/config) — env-based configuration as a general pattern
