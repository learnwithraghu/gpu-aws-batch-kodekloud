# Video 003 — Understanding Container Overrides and Runtime Parameters

**Section:** 006 — Running the End-to-End GPU Pipeline
**Lecture#:** 003
**Sheet title:** Understanding Container Overrides and Runtime Parameters
**Type:** Video
**Runtime target:** ~2 minutes
**Topic code:** 006-003-understanding-container-overri

---

The job definition is the stable contract. Container overrides supply the values that change for one run. We do not register a new definition for every vendor folder.

At submission time, KodeFood overrides the command with `python /app/describe_items.py`. It also passes the environment variables the script understands: `S3_BUCKET`, `S3_CSV_BUCKET`, `IMAGE_PREFIX`, and `BATCH_SIZE`.

The image, memory, and one-GPU requirement stay fixed. Only the stem changes: `images/sample` for one run, another vendor prefix for the next. A new folder of photos does not require a Docker rebuild. `BATCH_SIZE` changes how many images go through one GPU forward pass; it does not change the authoritative bucket.

This is where the S3 contract helps. Prefixes parameterize the work, and overrides deliver those parameters to the process. The job role still controls what S3 permits. Overrides only select keys within that permission boundary. If the role is healthy but the prefix is wrong, permissions can succeed while the catalog remains empty.

This split also supports larger parameterized workloads: keep the heavy execution contract stable and vary the small submission payload.

Be deliberate about resource overrides. Changing memory or GPU count can recreate the placement trap. In particular, do not replace `12288` MiB with `16384` MiB on `g4dn.xlarge`. Prefer varying data parameters unless you intentionally designed a different capacity profile.

One definition can therefore caption many vendors: the prefix and runtime values change, while the execution contract remains stable.

Next, we account for the time between a correct submission and the first caption.

---

## Further reading (not spoken)

- [AWS Batch: Container overrides](https://docs.aws.amazon.com/batch/latest/APIReference/API_ContainerOverrides.html) — command and environment overrides
- [AWS Batch: SubmitJob environment](https://docs.aws.amazon.com/batch/latest/APIReference/API_SubmitJob.html) — runtime parameters on submit
- [Twelve-Factor App: Config](https://12factor.net/config) — env-based configuration as a general pattern
