# Plan — Lesson 03 caption job

Completed 2026-09-28. Nothing pending.

`04-submit-and-wait --batch-stem sample` reached `SUCCEEDED` on
`gpu-teaching-caption-job:3`. `05-show-captions` printed one row:

> a note with the words invoe and a stamp

The container needed S3 access, so revision 3 sets `jobRoleArn` to
`gpu-teaching-batch-job-role` (12288 MiB, 1 GPU). Names live in
[`docs/aws-batch-setup.md`](docs/aws-batch-setup.md).
