FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOST=0.0.0.0 \
    PORT=8000 \
    SAMPLE_DIR=/app/images \
    UPLOAD_DIR=/app/uploads \
    AWS_REGION=ap-northeast-1 \
    S3_BUCKET=kodefood-menu-uploads-kodekloud \
    S3_PREFIX=uploads

WORKDIR /app

COPY 03-s3-upload/03b-restaurant-portal-s3/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY 03-s3-upload/03b-restaurant-portal-s3/app.py ./
COPY 03-s3-upload/03b-restaurant-portal-s3/static ./static
COPY 03-s3-upload/03b-restaurant-portal-s3/templates ./templates
COPY images ./images

RUN useradd --create-home --shell /bin/sh appuser \
    && mkdir -p /app/uploads \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["python", "app.py"]
