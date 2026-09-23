# Plan — Trigger Batch captioning → captions in S3 (resume point)

## Where we are

Done ✅ (all committed & pushed to `origin/main`):

| Commit | Change |
|---|---|
| `625e65f` | Lesson 03 step 00 `register-job-def` + README; `.env.example` updated with real resource names; lesson README lists step 00 |
| `554b81e` | Fix: re-describe job def after registering (API omits `containerProperties`) |
| `1cffd9d` | Fix: job def memory 16384 → 12288 MiB (full-instance memory can't be placed — `MISCONFIGURATION:JOB_RESOURCE_REQUIREMENT`); script now re-registers a revision whenever desired config changes |
| `072aacf` | Fix: `Dockerfile` pins `transformers==4.46.3` — newer transformers disable PyTorch on torch 2.1 base (`BlipForConditionalGeneration requires the PyTorch library`) |

Live AWS state (region `ap-northeast-1`, account `666234783044`) — all verified:

- ECR repo `gpu-teaching` exists (image `:latest` is the OLD build — needs rebuild)
- Images bucket `gpu-teaching-images-666234783044` has 1 image: `images/sample/Screenshot 2026-08-31 at 10.34.56 AM.png`
- Captions bucket `gpu-teaching-captions-csv-666234783044` exists (empty target)
- Spot queue `gpu-teaching-gpu-smoke-queue-spot` (g4dn.xlarge, cap-optimized, maxvCpus=4)
- Job def `gpu-teaching-caption-job:2` ACTIVE — image: course ECR URI, 4 vCPU · 12 GiB · 1 GPU
- Local untracked `.env` (gitignored) has all real values
- Docker 29.8.0 available; AWS CLI configured

Diagnosis trail (3 job failures, each solved in turn):

1. `MISCONFIGURATION:JOB_RESOURCE_REQUIREMENT` → job def asked for full 16 GiB; ECS never registers full instance memory → fixed with 12 GiB (rev :2 confirmed RUNNING was reached)
2. `RUNNABLE` stuck ~8 min then FAIL was the same resource misconfig on the first two submissions
3. Container exit 1 mid-run → CloudWatch showed transformers≥4.57 won't run on torch 2.1.0 → Dockerfile pin committed, **image not yet rebuilt**

## Remaining steps (in order)

### 1. Rebuild & push the image to ECR
```bash
bash helpers/push_ecr_image.sh
```
- Ensures ECR repo, docker login, build, tag, push `:latest`, writes `ECR_IMAGE_URI` to `.env`
- Takes ~5–10 min (CUDA base image + pip layer); `--pull` fetches fresh base
- Job def `:2` needs no change — same tag URI; new jobs pull the fresh image
- Rule: everything is already committed (`072aacf`), so safe to build now

### 2. Resubmit & wait for the caption job
```bash
cd lessons/03-images-to-captions/04-submit-and-wait
uv run --with boto3 --with python-dotenv python main.py --batch-stem sample
```
- Expect: SUBMITTED → RUNNABLE (up to ~5 min spot capacity wait) → STARTING → RUNNING → SUCCEEDED
- Job pulls new image, downloads BLIP (~1 GB, may print HF rate-limit warning — harmless), captions the PNG, writes:
  `s3://gpu-teaching-captions-csv-666234783044/captions/sample/captions.csv`

### 3. Verify output
```bash
cd ../05-show-captions
uv run --with boto3 --with python-dotenv python main.py --batch-stem sample
```
- Expect a table printing `1 captions in s3://gpu-teaching-captions-csv-666234783044/captions/sample/captions.csv`
  with the image URI + BLIP caption
- Cross-check via console/CLI if desired

### 4. If something still fails — debugging quick reference
```bash
# statusReason
aws batch describe-jobs --jobs <job-id> --region ap-northeast-1 \
  --query 'jobs[0].[status,statusReason,attempts[0].container.exitCode,attempts[0].container.logStreamName]'

# container logs
aws logs get-log-events --log-group-name /aws/batch/job \
  --log-stream-name 'gpu-teaching-caption-job/default/<taskId>' --region ap-northeast-1
```
- RUNNABLE forever → spot capacity; fallback `BATCH_JOB_QUEUE=gpu-teaching-gpu-smoke-queue-on-demand` in `.env`
- Exit 1 → read logs first; each fix → **commit to GitHub before rerunning** (user's standing rule)

### 5. Wrap-up (optional, after SUCCEEDED)
- Post a follow-up commit if any fixes were needed
- g4dn.xlarge Spot ≈ $0.21/hr in ap-northeast-1; ~10–15 min job ≈ pennies; `minvCpus=0` = no idle cost
- Optionally clean failed job history? (nothing to delete — Batch keeps failed jobs in history only)
