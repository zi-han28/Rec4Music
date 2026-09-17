FROM python:3.11-slim

WORKDIR /app

# System deps needed to build some Python packages (e.g. tokenizers, scikit-learn)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Pre-download the sentiment model at BUILD time, not at container startup.
# This avoids a slow first request and removes a runtime dependency on
# HuggingFace's servers being reachable when your app boots.
RUN python -c

EXPOSE 8000

# Railway injects a $PORT env var at runtime — the app must bind to it,
# not a hardcoded port, or the deploy will fail health checks.
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]