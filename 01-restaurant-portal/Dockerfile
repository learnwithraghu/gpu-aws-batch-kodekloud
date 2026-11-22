FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOST=0.0.0.0 \
    PORT=8000 \
    SAMPLE_DIR=/app/images \
    UPLOAD_DIR=/app/uploads

WORKDIR /app

COPY 01-restaurant-portal/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY 01-restaurant-portal/app.py ./
COPY 01-restaurant-portal/static ./static
COPY 01-restaurant-portal/templates ./templates
COPY images ./images

RUN useradd --create-home --shell /bin/sh appuser \
    && mkdir -p /app/uploads \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["python", "app.py"]
