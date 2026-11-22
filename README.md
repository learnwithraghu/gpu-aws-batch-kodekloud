# KodeFood on AWS Batch

Two parts.

**[01 — Restaurant portal](01-restaurant-portal/)** is the back office a restaurant uses today. Staff upload a dish photo, type the name of that photo, and choose **Update our menu**. The page tells them someone from the menu team will review it and update the menu within 24 hours. It runs in Docker — see its README for cleanup, build, and run commands.

**[02 — AWS Batch](02-aws-batch/)** is the console path that replaces that wait: a compute environment, a job queue, a job definition, one job, then the same three pieces again for a GPU on Spot. Each step is a folder with a click-by-click guide.

Sample dish photos are in [`images/`](images/).

Live resource names for this AWS account stay in [`docs/aws-batch-setup.md`](docs/aws-batch-setup.md). The console walkthrough creates a separate `kodefood-*` stack and does not change `gpu-teaching-*`.

Agent instructions are in [`AGENTS.md`](AGENTS.md). The transcript skill is in [`.agents/skills/tone/`](.agents/skills/tone/). Both are editor-neutral.
