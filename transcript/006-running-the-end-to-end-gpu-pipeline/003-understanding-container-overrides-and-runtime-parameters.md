# Video 003 — Understanding Container Overrides and Runtime Parameters

**Section:** 006 — Running the End-to-End GPU Pipeline
**Lecture#:** 003
**Sheet title:** Understanding Container Overrides and Runtime Parameters
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 006-003-understanding-container-overri

---

The job definition is the stable recipe. Container overrides are the per-run knobs. If you rebuild the definition for every vendor folder, you will drown in revisions.

At submit time, KodeFood overrides the command to `python /app/describe_items.py` and passes environment variables the script already understands: `S3_BUCKET`, `S3_CSV_BUCKET`, `IMAGE_PREFIX`, and `BATCH_SIZE`. Same image, same memory, same GPU requirement — different stem. Today `images/sample`, tomorrow another vendor prefix. No Docker rebuild required for a new folder of photos. `BATCH_SIZE` only changes how many images ride in one GPU forward pass; it does not change which bucket is authoritative.

That is the point of the S3 contract you built earlier. Prefixes parameterize work. Overrides deliver those parameters into the process environment. The job role still governs what S3 allows; overrides only choose which keys to touch inside that allowance. Wrong prefix with a healthy role still yields an empty catalog — the permissions worked; the path did not.

Teams that run thousands of Batch array or parameterized jobs — genomics pipelines, media transcodes, retail catalog refreshers — rely on this split. Shopify-scale and smaller shops alike: pin the heavy definition, vary the lightweight submit payload.

Be careful what you override. Changing memory or GPU count in a careless override can recreate the sixteen-gibibytes placement trap. Prefer varying data parameters, not resource shape, unless you intend a new capacity profile.

So when someone asks “how does one job definition caption many vendors?” the answer is overrides plus prefixes — not a new registration per folder.

Next we confront the clock: even a correct submit pays cold-start time before the first caption appears.

---

## Further reading (not spoken)

- [AWS Batch: Container overrides](https://docs.aws.amazon.com/batch/latest/APIReference/API_ContainerOverrides.html) — command and environment overrides
- [AWS Batch: SubmitJob environment](https://docs.aws.amazon.com/batch/latest/APIReference/API_SubmitJob.html) — runtime parameters on submit
- [Twelve-Factor App: Config](https://12factor.net/config) — env-based configuration as a general pattern
