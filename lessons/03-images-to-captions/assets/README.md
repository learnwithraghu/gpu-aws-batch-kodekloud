# Sample Images

Place a handful (5–20) of `.jpg`/`.jpeg`/`.png` images here, in
`assets/images/`.

**How to get some:**

Option A — Download a few free Creative Commons photos from
[Pexels](https://www.pexels.com/) or [Unsplash](https://unsplash.com/), e.g.:
```bash
mkdir -p assets/images
curl -L "https://images.pexels.com/photos/58997/pexels-photo-58997.jpeg" -o assets/images/sample_01.jpg
```

Option B — Use any `.jpg`/`.png` photos you already have. Keep the folder
small (a few MB) for fast uploads.

> **Tip**: `submit_job.py` uploads every image in `assets/images/` to S3
> automatically — you don't need to do anything else.

