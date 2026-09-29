# FROM python:3.11-slim

# WORKDIR /app

# # System deps needed to build some Python packages (e.g. tokenizers, scikit-learn)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# EXPOSE 8000

# # Railway injects a $PORT env var at runtime — the app must bind to it,
# # not a hardcoded port, or the deploy will fail health checks.
# CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies, including wget to download the model
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download the model directly into the container (adjust the URL to your specific Hugging Face source)
RUN wget -q -O Llama-3.2-1B-Instruct-Q6_K.gguf https://huggingface.co/bartowski/Llama-3.2-1B-Instruct-GGUF/resolve/main/Llama-3.2-1B-Instruct-Q6_K.gguf

COPY . .

EXPOSE 8000

# Railway injects a $PORT env var at runtime
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]