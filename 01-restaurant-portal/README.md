# Restaurant portal

This is the KodeFood back office. A restaurant adds dish photos, types the name of each photo, and sends the batch to the menu team. The team reviews the photos by hand and updates the customer menu within 24 hours.

Sample photos from the repo `images/` folder are baked into the Docker image, so run all Docker commands from the **repo root**.

## Clean up before building

Remove any old container, image, and dangling build cache before a clean rebuild (safe to run even if nothing exists yet):

```bash
docker rm -f kodefood-restaurant-portal 2>/dev/null || true
docker rmi -f kodefood-restaurant-portal:latest 2>/dev/null || true
docker builder prune -f
```

## Build the image

From the repo root:

```bash
docker build -f 01-restaurant-portal/Dockerfile -t kodefood-restaurant-portal:latest .
```

To force a completely fresh rebuild without layer caching:

```bash
docker build --no-cache -f 01-restaurant-portal/Dockerfile -t kodefood-restaurant-portal:latest .
```

## Run it

Detached in the background:

```bash
docker run -d --name kodefood-restaurant-portal -p 8000:8000 kodefood-restaurant-portal:latest
```

Or in the foreground (`--rm` removes the container when you stop it with `Ctrl+C`):

```bash
docker run --rm --name kodefood-restaurant-portal -p 8000:8000 kodefood-restaurant-portal:latest
```

Open http://127.0.0.1:8000 (if port `8000` is already in use, map another host port such as `-p 8080:8000`).

## Logs, stop, and cleanup

Follow container logs:

```bash
docker logs -f kodefood-restaurant-portal
```

Stop and remove the running container:

```bash
docker rm -f kodefood-restaurant-portal
```

Full cleanup (container and image):

```bash
docker rm -f kodefood-restaurant-portal 2>/dev/null || true
docker rmi -f kodefood-restaurant-portal:latest 2>/dev/null || true
```

## What to click

1. Pick a sample photo, or upload your own.
2. Write the name of that photo.
3. Choose **Add to this update**. Repeat for each dish.
4. Choose **Update our menu**.

The page then says someone from the menu team will review the photos and update the menu within 24 hours. **Start another update** clears the desk so you can run it again.
