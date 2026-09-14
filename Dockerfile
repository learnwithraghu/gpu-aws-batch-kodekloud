# ─────────────────────────────────────────────────────────────────
#  Shared Docker image for ALL GPU Teaching lessons
#  Built once, used by every AWS Batch job.
#
#  Base: official PyTorch image with CUDA 11.8 (matches g4dn GPU driver)
# ─────────────────────────────────────────────────────────────────
FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

# Install Python dependencies for all lessons in one layer
RUN pip install --no-cache-dir \
    openai-clip==1.0        \
    opencv-python-headless  \
    boto3>=1.43.93          \
    python-dotenv           \
    numpy

# Copy lesson scripts into the image
# Batch overrides the "command" field to run the right lesson script
WORKDIR /app
COPY lessons/ /app/lessons/
COPY helpers/s3_vectors.py /app/helpers/s3_vectors.py
