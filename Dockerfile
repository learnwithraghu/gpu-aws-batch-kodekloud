# ─────────────────────────────────────────────────────────────────
#  Shared Docker image for ALL GPU Teaching lessons
#  Built once, used by every AWS Batch job.
#
#  Base: official PyTorch image with CUDA 11.8 (matches g4dn.xlarge NVIDIA T4 driver)
# ─────────────────────────────────────────────────────────────────
FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

# Install Python dependencies for all lessons in one layer
# transformers provides BLIP (image captioning)
RUN pip install --no-cache-dir \
    transformers>=4.42      \
    Pillow                  \
    boto3                   \
    python-dotenv

# Copy lesson scripts into the image
# Batch overrides the "command" field to run the right lesson script
WORKDIR /app
COPY lessons/ /app/lessons/
