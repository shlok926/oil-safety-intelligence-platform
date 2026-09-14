# ==============================================================================
# OIL Safety Intelligence Platform — Backend Dockerfile
# Python 3.11 Slim Multi-Stage Build
# ==============================================================================

FROM python:3.11-slim as builder

WORKDIR /build

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# --- Runtime Stage ---
FROM python:3.11-slim as runner

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/home/oil_user/.local/bin:$PATH \
    PYTHONPATH=/app \
    MODEL_CACHE_DIR=/app/models/cache

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Non-root user for enterprise security
RUN groupadd -g 1001 oil_group && \
    useradd -u 1001 -g oil_group -m -s /bin/bash oil_user

# Create model cache directory contract (assets provisioned in later phase)
RUN mkdir -p /app/models/cache && chown -R oil_user:oil_group /app

COPY --from=builder --chown=oil_user:oil_group /root/.local /home/oil_user/.local
COPY --chown=oil_user:oil_group backend/ /app/backend/

USER oil_user

WORKDIR /app

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
