FROM python:3.10-slim

# Install system dependencies for OpenCV and image processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set up user for Hugging Face Spaces / secure container execution
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    PYTHONUNBUFFERED=1

WORKDIR $HOME/app

# Pre-install CPU-only PyTorch and torchvision to optimize image size & memory
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Install project dependencies
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and model weights
COPY --chown=user . .

# Cloud platforms typically set PORT (Hugging Face Spaces defaults to 7860)
ENV PORT=7860
EXPOSE 7860

CMD ["python", "app.py"]
