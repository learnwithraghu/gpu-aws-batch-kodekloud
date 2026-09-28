# Lesson 09 — Theory

The GPU job is over. The product is an object in S3.

## Consuming Batch outputs

The food app never calls `SubmitJob`. It never polls Batch statuses. It reads `descriptions/<batch>/descriptions.csv` from the CSV bucket (or a copy exported elsewhere).

That split matters in real systems: Batch is an offline worker. Downstream services depend on the artifact contract, not on the scheduler API. If the CSV is missing, the app is broken even though yesterday’s job “succeeded” on a different stem.

## CSV as an interface

Stable columns are an API:

```csv
image_s3_uri,item_description
```

Rename a column without updating the app and you break consumers. Adding columns carefully can be fine; silently changing meaning of `item_description` is not. Treat this file like a small public schema for the catalog.

## Row count as a check

`wc -l` on the CSV counts header + data rows. Subtract one for the header. That number should match how many `.jpg` / `.jpeg` / `.png` keys the job listed under the prefix.

Fewer rows → skipped extensions, failed mid-job (should not write a partial file in this design), or wrong stem. More rows than you expected → extra photos in the prefix you did not notice in lesson 06.

## When to re-run

| Change | Rebuild image? | Re-upload? | Resubmit? |
|--------|----------------|------------|-----------|
| New photos in the same folder | No | Yes (sync) | Yes |
| Better prompt / generate settings | Yes (03–04) | No | Yes |
| Job `FAILED` after a fix | Only if code/image changed | If data was wrong | Yes |
| Only want to re-read the CSV | No | No | No |

Re-running overwrites the same key for that stem. That is intentional for this course: latest successful catalog wins.

## What you learned end-to-end

You can now walk a real GPU batch path:

1. **Data** — S3 prefixes for photos and CSV (05–06, 09)
2. **Program** — container code split I/O vs GPU (02)
3. **Image** — build amd64, pin deps (03)
4. **Registry** — ECR push so instances can pull (04)
5. **Scheduler** — GPU CE, queue, job definition, roles (01, 07)
6. **Run** — submit, wait, debug statuses and logs (08)

Checklist for the next vendor folder: sync to `images/<stem>/`, submit with matching `IMAGE_PREFIX`, confirm `SUCCEEDED`, read `descriptions/<stem>/descriptions.csv`. Rebuild only when the container program or Dockerfile changed.
