# Lesson 06 — Submit and wait

One command submits one folder and polls until the job finishes. The folder must already be in the images bucket (lesson 02).

## What `--batch-stem sample` means

The stem is the folder name under `images/`. `sample` means the container reads `images/sample/` and writes `descriptions/sample/descriptions.csv`.

## The command

```bash
python submit_job.py --batch-stem sample
```

That submits `python /app/describe_items.py` on `BATCH_JOB_QUEUE` using `BATCH_JOB_DEFINITION` from `.env`. `--batch-size` defaults to 8 and only changes how many photos the GPU sees at once.

## Status path

The script prints a status about every 10 seconds:

`SUBMITTED` → `RUNNABLE` → `STARTING` → `RUNNING` → `SUCCEEDED`

The first run on a new instance also downloads the BLIP weights. A job that sits in `RUNNABLE` for several minutes is usually Spot capacity. The fallback queue is `gpu-teaching-gpu-smoke-queue-on-demand` (`BATCH_JOB_QUEUE` in `.env`).

A failed job still exits the script. The reason is in CloudWatch `/aws/batch/job`, not in the final status line alone.

## Where the file lands

On success the script prints:

```
descriptions/<batch-stem>/descriptions.csv
```

in the CSV bucket. One folder in, one file out. Lesson 07 prints the rows.
