# GPU image for the food-item description job (g4dn.xlarge → CUDA 11.8 / T4).
FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

WORKDIR /app

COPY requirements-gpu.txt .
RUN pip install --no-cache-dir -r requirements-gpu.txt

COPY lessons/02-the-container-program/describe_items.py /app/describe_items.py
