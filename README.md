# KodeFood on AWS Batch

Four parts.

**[01 — Restaurant portal](01-restaurant-portal/)** is the back office a restaurant uses today. Staff upload a dish photo, type the name of that photo, and choose **Update our menu**. The page tells them someone from the menu team will review it and update the menu within 24 hours. It runs in Docker — see its README for cleanup, build, and run commands.

**[02 — AWS Batch](02-aws-batch/)** is the console path that replaces that wait: a compute environment, a job queue, a job definition, one job, then the same three pieces again for a GPU on Spot. Each step is a folder with a click-by-click guide.

**[03 — Upload portal photos to S3](03-s3-upload/)** links the portal to Amazon S3: `03a` creates the private S3 bucket in Tokyo, and `03b` runs the same restaurant portal from `01` with S3 upload wired in so photos land in S3 for a later AWS Batch GPU scoring step.

**[04 — ML menu satisfaction scorer](04-menu-scorer/)** builds a minimal ML scoring script that rates dish photos from 1.0 to 10.0 (`>= 8.0` approved for the app, `< 8.0` rejected) and tests it locally against `images/` before running on AWS Batch in step 05.

Sample dish photos are in [`images/`](images/).

Live resource names for this AWS account stay in [`docs/aws-batch-setup.md`](docs/aws-batch-setup.md). The console walkthrough creates a separate `kodefood-*` stack and does not change `gpu-teaching-*`.

Agent instructions are in [`AGENTS.md`](AGENTS.md). The transcript skill is in [`.agents/skills/tone/`](.agents/skills/tone/). Both are editor-neutral.
